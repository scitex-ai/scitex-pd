"""Smoke: ``force_df`` coerces a dict in a subprocess (PS-211).

Subprocess-driven (``sys.executable -c ...``) so this proves the
installed package resolves its hard dependencies — an in-process call
would not. Hermetic: pandas/numpy are hard deps, no network, no
credentials, no writes outside tmp dirs.
"""

from __future__ import annotations

import subprocess
import sys

import pytest

pytestmark = pytest.mark.smoke

CODE = "\n".join(
    [
        "import scitex_pd as pd_",
        "df = pd_.force_df({'a': [1, 2]})",
        "print(df.shape)",
    ]
)


def test_force_df_roundtrip_in_subprocess() -> None:
    # Arrange
    argv = [sys.executable, "-c", CODE]

    # Act
    completed = subprocess.run(argv, capture_output=True, text=True, timeout=30)

    # Assert
    assert (completed.returncode, completed.stdout.strip()) == (0, "(2, 1)")
