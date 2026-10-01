"""E2E: coerce → transform pipeline on real DataFrames (PS-212).

No network, no mocks — drives the real helpers end to end. Gated on
``RUN_E2E=1`` so the default unit run stays fast.
"""

from __future__ import annotations

import os

import pytest

pytestmark = [pytest.mark.e2e, pytest.mark.skipif(os.environ.get("RUN_E2E") != "1", reason="RUN_E2E!=1")]


def test_coerce_transform_pipeline_roundtrip() -> None:
    pd = pytest.importorskip("pandas")
    import scitex_pd as pd_

    # Arrange
    raw = {"b": [1.234, 5.678], "a": ["x", "y"]}

    # Act
    df = pd_.force_df(raw)
    df = pd_.round(df, 1)
    df = pd_.mv(df, "a", -1)

    # Assert
    assert (list(df.columns)[-1], df["b"].tolist()) == ("a", [1.2, 5.7])
