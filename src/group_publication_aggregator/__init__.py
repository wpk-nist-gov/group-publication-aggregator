"""
Top level API (:mod:`group_publication_aggregator`)
======================================================
"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _version

from .core import example_function

try:
    __version__ = _version("group-publication-aggregator")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "999"


__author__ = """William P. Krekelberg"""
__email__ = "wpk@nist.gov"


__all__ = [
    "__version__",
    "example_function",
]
