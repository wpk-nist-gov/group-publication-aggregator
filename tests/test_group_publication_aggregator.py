"""Tests for `group-publication-aggregator` package."""

from __future__ import annotations


def test_version() -> None:
    from group_publication_aggregator import __version__

    assert __version__ != "999"
