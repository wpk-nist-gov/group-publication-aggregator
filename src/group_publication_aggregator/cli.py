"""Command line interface"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import TYPE_CHECKING, cast

import pandas as pd

if TYPE_CHECKING:
    from collections.abc import Sequence
    from typing import Any

    from ._typing import Style

    class _Params:
        """Dummy class for typing argparse"""

        semi: list[int]
        first: list[int]
        excel_path: Path
        sheet: str
        year: int
        quarter: int
        render: str | None


def get_parser() -> argparse.ArgumentParser:
    """Get base parser."""
    parser = argparse.ArgumentParser(
        prog="pub-agg",
        description="Program to aggregate group publications/talks",
    )

    parser.add_argument("--year", "-y", default=2025, type=int, help="Year to query")
    parser.add_argument("--quarter", "-q", default=1, type=int, help="Querter to query")

    parser.add_argument(
        "--semi",
        default=[],
        type=int,
        action="append",
        help="Row numbers that have a semicolon",
    )
    parser.add_argument(
        "--first",
        default=[],
        type=int,
        action="append",
        help="Row numbers that have initial lastname format.",
    )
    parser.add_argument(
        "--render",
        "-r",
        default=None,
        choices=["paper", "talk", None],
        help="How to render",
    )

    parser.add_argument("excel_path", type=Path, help="file or paths to open")
    parser.add_argument(
        "sheet", default="papers", type=str, help="file or paths to open", nargs="?"
    )
    return parser


def _format_paper(df: pd.DataFrame) -> list[str]:
    data: list[str] = []
    row: pd.Series[Any]
    for _, row in df.iterrows():  # pyright: ignore[reportUnknownMemberType, reportUnknownVariableType, reportAssignmentType]
        out = "{authors}, {title}, {ref}".format(
            authors=row["Authors"],
            title=row["Title"],
            ref=row["Reference"],  # pyright: ignore[reportUnknownArgumentType]
        )

        if not row.isna()["Doi"]:
            out += ", {}".format(row["Doi"])
        data.append(out)
    return data


def _format_talk(df: pd.DataFrame) -> list[str]:
    df = df.assign(  # pyright: ignore[reportUnknownMemberType]
        month_year=lambda x: x["Date"].dt.month_name()  # pyright: ignore[reportUnknownMemberType, reportUnknownLambdaType]
        + " "
        + x["Date"].dt.year.astype(str)  # pyright: ignore[reportUnknownMemberType]
    )

    data: list[str] = []
    row: pd.Series[Any]
    for _, row in df.iterrows():  # pyright: ignore[reportUnknownMemberType]
        out = "{authors}, {title}, {ref}, {loc}, {date} ({Type})".format(
            authors=row["Authors"],
            title=row["Title"],
            ref=row["Conference"],
            loc=row["Location"],
            date=row["month_year"],
            Type=row["Type"],
        )

        data.append(out)
    return data


def _to_bullet(s: Sequence[str]) -> str:
    return "\n".join([f"* {x}" for x in s])


def main(
    args: Sequence[str] | None = None,
) -> int:
    """Console script for open_notebook."""
    # get cli options
    parser = get_parser()
    options = cast(
        "_Params", parser.parse_args() if args is None else parser.parse_args(args)
    )
    frame: pd.DataFrame = (
        pd.read_excel(options.excel_path, options.sheet)  # pyright: ignore[reportUnknownMemberType]
        .dropna(how="all")
        .pipe(
            lambda df: df[
                (df["Fiscal Year"] == options.year) & (df["Quarter"] == options.quarter)
            ]
        )
    )

    if "Date" in frame:
        frame = frame.astype({"Date": "datetime64[ns]"})  # pyright: ignore[reportUnknownMemberType]

    styles: list[Style] = [None] * len(frame)

    for i in options.semi:
        styles[i] = "semi"

    for i in options.first:
        styles[i] = "first"

    if any(_ is not None for _ in styles):
        from .core import apply_by_row

        frame["Authors"] = apply_by_row(cast("Sequence[str]", frame["Authors"]), styles)

    if options.render == "paper":
        print(_to_bullet(_format_paper(frame)))

    elif options.render == "talk":
        print(_to_bullet(_format_talk(frame)))

    else:
        with pd.option_context("display.max_columns", 100):
            print(frame)

    return 0
