"""
-----------
Basic Usage
-----------

A short example showcasing how to use the library. The docstrings will be
turns in REST by sphinx-gallery.
"""

import matplotlib.pyplot as plt
import numpy as np

from mpl_point_clicker import clicker

image = np.load('example_image.npy')

fig, ax = plt.subplots()
ax.imshow(image, cmap='gray')
klicker = clicker(ax, ['cells', 'pdms', 'media'], markers=['o', 'x', '*'])
plt.show()


print(klicker.get_positions())
