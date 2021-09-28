"""
---------
Callbacks
---------

Demonstration of how to set up callback functions.

"""

from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np

from mpl_point_clicker import clicker

image = np.load("example_image.npy")

fig, ax = plt.subplots()
ax.imshow(image, cmap='gray')
klicker = clicker(ax, ['cells', 'pdms', 'media'], markers=['o', 'x', '*'])


def class_changed_cb(new_class: str):
    print(f'The newly selected class is {new_class}')


def point_added_cb(position: Tuple[float, float], klass: str):
    x, y = position
    print(f"New point of class {klass} added at {x=}, {y=}")


def point_removed_cb(position: Tuple[float, float], klass: str, idx):
    x, y = position

    suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(idx, 'th')
    print(
        f"The {idx}{suffix} point of class {klass} with position {x=:.2f}, {y=:.2f}  was removed"
    )


klicker.on_class_changed(class_changed_cb)
klicker.on_point_added(point_added_cb)
klicker.on_point_removed(point_removed_cb)


plt.show()


print(klicker.get_positions())
