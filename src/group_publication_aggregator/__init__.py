"""
Top level API (:mod:`group_publication_aggregator`)
======================================================
"""

from importlib.metadata import PackageNotFoundError
from importlib.metadata import version as _version

from .core import apply_by_row, first_initials_to_final, semicolon_to_final

try:
    __version__ = _version("group-publication-aggregator")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "999"


__author__ = """William P. Krekelberg"""
__email__ = "wpk@nist.gov"


__all__ = [
    "__version__",
    "apply_by_row",
    "first_initials_to_final",
    "semicolon_to_final",
]
