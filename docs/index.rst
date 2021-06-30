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

.. code-block:: python

   fig, ax = plt.subplots(constrained_layout=True)
   image = np.random.rand(512, 512)
   ax.imshow(image, cmap="gray")
   klicker = clicker(
      ax,
      ["cell", "pdms", "media"],
      markers=["o", "x", "*"]
   )

You can then access the positions via ``klicker.get_positions``.



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
