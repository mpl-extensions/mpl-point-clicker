#!/usr/bin/env python

# Copyright (c) Ian Hunt-Isaak.
# Distributed under the terms of the Modified BSD License.

__all__ = [
    "clicker",
]
from numbers import Integral

import numpy as np
from matplotlib.backend_bases import MouseButton
from matplotlib.cbook import CallbackRegistry


class clicker:
    def __init__(
        self,
        ax,
        classes,
        init_class=None,
        markers=None,
        colors=None,
        legend_bbox=(1.04, 1),
        legend_loc="upper left",
        pick_dist=10,
        **line_kwargs,
    ):
        """
        Parameters
        ----------
        ax : matplotlib axis
        classes : int or list
        init_class : int, or str, optional
            The initial class to use, otherwise will be the first
            class in *classes*
        markers : list
            The marker styles to use.
        colors : list
        legend_bbox : tuple
            bbox to use for the legend
        legend_loc : str or int
            loc to use for the legend
        pick_dist : int
            Picker distance for legend
        **line_kwargs : kwargs
            Line2D objects (from ax.plot) are used to generate the markers.
            line_kwargs will be passed through to all of the `ax.plot` calls.
        """
        if isinstance(classes, Integral):
            self._classes = list(range(classes))
        else:
            self._classes = classes

        if init_class is None:
            self._current_class = self._classes[0]
        else:
            if init_class not in self._classes:
                raise ValueError(
                    f"init_class must be a valid class. Got {init_class} "
                    f"while valid classes are {self._classes}"
                )
            self._current_class = init_class

        if colors is None:
            colors = [None] * len(self._classes)
        if markers is None:
            markers = ["o"] * len(self._classes)

        self.ax = ax
        self._lines = {}
        linestyle = line_kwargs.pop("linestyle", "")
        for i, c in enumerate(self._classes):
            (self._lines[c],) = self.ax.plot(
                [],
                [],
                color=colors[i],
                marker=markers[i],
                label=c,
                linestyle=linestyle,
                **line_kwargs,
            )
        self._leg = self.ax.legend(bbox_to_anchor=legend_bbox, loc=legend_loc)
        self._leg_artists = {}
        self._class_leg_artists = {}
        for legline, legtext, klass in zip(
            self._leg.get_lines(), self._leg.get_texts(), self._classes
        ):
            legline.set_picker(pick_dist)
            legtext.set_picker(pick_dist)
            self._leg_artists[legtext] = klass
            self._leg_artists[legline] = klass
            try:
                # mpl < 3.5
                self._class_leg_artists[klass] = (legline, legline._legmarker, legtext)
            except AttributeError:
                self._class_leg_artists[klass] = (legline, legtext)

        self._fig = self.ax.figure
        self._fig.canvas.mpl_connect("button_press_event", self._clicked)
        self._fig.canvas.mpl_connect("pick_event", self._on_pick)
        self._positions = {c: [] for c in self._classes}
        self._update_legend_alpha()
        self._observers = CallbackRegistry()

    def get_positions(self):
        return {k: np.asarray(v) for k, v in self._positions.items()}

    def set_positions(self, positions):
        """
        Set the current positions for all classes.

        Parameters
        ----------
        positions : dict
            A dictionary with strings as keys and 2D array-like values. The values
            will be interpreted as (N, 2) with x, y as the columns. The keys in
            the dictionary must all be valid classes. If a class is not included in
            *positions* then the existing values will not be modified.
        """
        # check all keys first so we don't partially overwrite data
        for k in positions.keys():
            if k not in self._classes:
                raise ValueError(f"class {k} is not in {self._classes}")

        for k, v in positions.items():
            self._positions[k] = list(v)
        self._observers.process('pos-set', self.get_positions())

    def _on_pick(self, event):
        # On the pick event, find the original line corresponding to the legend
        # proxy line, and toggle its visibility.
        try:
            klass = self._leg_artists[event.artist]
        except KeyError:
            # some pick event not on our legend
            return
        self._current_class = klass
        self._update_legend_alpha()
        self._observers.process('class-changed', klass)

    def _update_legend_alpha(self):
        for c in self._classes:
            alpha = 1 if c == self._current_class else 0.2
            for a in self._class_leg_artists[c]:
                a.set_alpha(alpha)
        self._fig.canvas.draw()

    def _has_cbs(self, name):
        """return whether there are callbacks registered for the current class"""
        try:
            return len(self._observers.callbacks[name]) > 0
        except KeyError:
            return False

    def _clicked(self, event):
        if not self._fig.canvas.widgetlock.available(self):
            return
        if event.inaxes is self.ax:
            if event.button is MouseButton.LEFT:
                self._positions[self._current_class].append((event.xdata, event.ydata))
                self._update_points(self._current_class)
                self._observers.process(
                    'point-added',
                    (event.xdata, event.ydata),
                    self._current_class,
                )
            elif event.button is MouseButton.RIGHT:
                pos = self._positions[self._current_class]
                if len(pos) == 0:
                    return
                dists = np.linalg.norm(
                    np.asarray([event.xdata, event.ydata])[None, None, :]
                    - np.asarray(pos)[None, :, :],
                    axis=-1,
                )
                idx = np.argmin(dists[0])
                removed = pos.pop(idx)
                self._update_points(self._current_class)
                self._observers.process(
                    'point-removed',
                    removed,
                    self._current_class,
                    idx,
                )

    def _update_points(self, klass=None):
        if klass is None:
            klasses = self._classes
        else:
            klasses = [klass]
        for c in klasses:
            new_off = np.array(self._positions[c])
            if new_off.ndim == 1:
                # no points left
                new_off = np.zeros([0, 2])
            self._lines[c].set_data(new_off.T)
        self._fig.canvas.draw()

    def on_point_added(self, func):
        """
        Connect *func* as a callback function to new points being added.
        *func* will receive the the position of the new point as a tuple (x, y), and
        the class of the new point.

        Parameters
        ----------
        func : callable
            Function to call when a point is added.

        Returns
        -------
        int
            Connection id (which can be used to disconnect *func*).
        """
        return self._observers.connect('point-added', lambda *args: func(*args))

    def on_point_removed(self, func):
        """
        Connect *func* as a callback function when points are removed.
        *func* will receive the the position of the new point, the class of the removed
        point, the point's index in the old list of points of that class, and the
        updated dictionary of all points.

        Parameters
        ----------
        func : callable
            Function to call when a point is removed

        Returns
        -------
        int
            Connection id (which can be used to disconnect *func*).
        """
        return self._observers.connect('point-removed', lambda *args: func(*args))

    def on_class_changed(self, func):
        """
        Connect *func* as a callback function when the current class is changed.
        *func* will receive the new class.

        Parameters
        ----------
        func : callable
            Function to call when the current class is changed.

        Returns
        -------
        int
            Connection id (which can be used to disconnect *func*).
        """
        self._observers.connect('class-changed', lambda klass: func(klass))

    def on_positions_set(self, func):
        """
        Connect *func* as a callback function when the *set_positions* function is
        called. *func* will receive the updated dictionary of all points.

        Parameters
        ----------
        func : callable
            Function to call when *set_positions* is called.

        Returns
        -------
        int
            Connection id (which can be used to disconnect *func*).
        """
        return self._observers.connect('pos-set', lambda pos_dict: func(pos_dict))
