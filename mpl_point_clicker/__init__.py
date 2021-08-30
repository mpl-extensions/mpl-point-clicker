#!/usr/bin/env python

# Copyright (c) Ian Hunt-Isaak.
# Distributed under the terms of the Modified BSD License.

try:
    from ._version import version as __version__
except ImportError:  # pragma: no cover
    __version__ = "unknown"
from ._clicker import clicker

__all__ = [
    "__version__",
    "clicker",
]
