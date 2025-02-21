"""
Core functionality (:mod:`~group_publication_aggregator.core`)
==============================================================
"""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

    from ._typing import Style


def first_initials_to_final(
    string: str,
    split_char: str = ",",
    inner_split: str = " ",
    join_char: str = ", ",
    inner_join: str = " ",
) -> str:
    """
    Convert first intial format to to final initial format

    Examples
    --------
    >>> s = "A.B. Women, C.D. Guy"
    >>> first_initials_to_final(s)
    'Women A.B., Guy C.D.'
    """
    out: list[str] = []
    for s in string.split(split_char):
        meta = s.split(inner_split)

        last_name = meta[-1].strip()
        first_name = "".join(meta[:-1])

        out.append(f"{last_name}{inner_join}{first_name}")

    return join_char.join(out)


def semicolon_to_final(
    string: str,
    split_char: str = ";",
    inner_split: str = ",",
    join_char: str = ", ",
    inner_join: str = " ",
) -> str:
    """
    Convert semicolon format to last first format.

    Examples
    --------
    >>> s = "Women, A.B.; Guy, C.D."
    >>> semicolon_to_final(s)
    'Women A.B., Guy C.D.'
    """
    out: list[str] = []
    for s in string.split(split_char):
        meta = s.split(inner_split)
        last_name = meta[0].strip()
        first_name = ("".join(meta[1:])).replace(" ", "")

        out.append(f"{last_name}{inner_join}{first_name}")

    return join_char.join(out)


def apply_by_row(
    rows: Iterable[str],
    styles: Iterable[Style] | Style = None,
) -> list[str]:
    """
    Apply a style to rows.

    Examples
    --------
    >>> rows = ["A.B. Women, C.D. Guy", "Women, A.B.; Guy, C.D."]
    >>> apply_by_row(rows, ["first", "semi"])
    ['Women A.B., Guy C.D.', 'Women A.B., Guy C.D.']

    """
    from itertools import repeat

    styles_: Iterable[Style]
    if styles is None:
        styles_ = repeat(None)
    elif isinstance(styles, str):
        styles_ = repeat(styles)
    else:
        styles_ = styles

    def func(row: str, style: Style) -> str:
        if style == "semi" or (style is None and ";" in row):
            return semicolon_to_final(row)

        if style == "first":
            return first_initials_to_final(row)

        return row

    return list(map(func, rows, styles_))
