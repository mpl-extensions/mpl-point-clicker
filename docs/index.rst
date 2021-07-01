Welcome to mpl_point_clicker's documentation!
===================================================================

A library for interactively labelling points with an arbitrary number of classes



.. image:: _static/images/front-page.apng

Installation
^^^^^^^^^^^^^

.. code-block:: bash

   pip install mpl_point_clicker

Usage
^^^^^

- Left-click to place a point
- Right click to remove the nearest point
- Left click on legend to change classes
- Get positions with ``.get_positions()``

.. code-block:: python

   import numpy as np
   import matplotlib.pyplot as plt
   from mpl_point_clicker import clicker

   fig, ax = plt.subplots(constrained_layout=True)
   image = np.random.rand(512, 512)
   ax.imshow(image, cmap="gray")
   klicker = clicker(
      ax,
      ["cell", "pdms", "media"],
      markers=["o", "x", "*"]
   )


You can also add scroll to zoom and middle-click and drag to pan with tools from
`mpl-interactions <https://mpl-interactions.readthedocs.io/en/stable/examples/zoom-factory.html>`_

.. code-block:: python

   from mpl_interactions import zoom_factory, panhandler

   fig, ax = plt.subplots(constrained_layout=True)
   image = np.random.rand(512, 512)
   ax.imshow(image, cmap="gray")

   # add zooming and middle click to pan
   zoom_factory(ax)
   ph = panhandler(fig, button=2)

   klicker = clicker(
      ax,
      ["cell", "pdms", "media"],
      markers=["o", "x", "*"]
   )



Getting Help
^^^^^^^^^^^^

If you have a question on how to do something with ``mpl_point_clicker`` a great place
to ask it is: https://discourse.matplotlib.org/c/3rdparty/18.

Reporting Issues
^^^^^^^^^^^^^^^^

Please report issues to https://github.com/ianhi/mpl-point-clicker/issues/new/choose

.. toctree::
   :maxdepth: 3

   examples/index
   API
   Contributing



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
