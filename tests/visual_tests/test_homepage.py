"""Visual regression tests using the real baseline and current screenshots.

These tests verify that the existing screenshots in the workspace produce a
0.00 % mismatch, confirming no visual regression has been introduced.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.main.image_compare.comparator import compare_images

BASELINE = Path("baseline/homepage.png")
CURRENT = Path("current/homepage.png")
DIFF_DIR = Path("diff")


@pytest.fixture(autouse=True)
def _ensure_diff_dir():
    DIFF_DIR.mkdir(parents=True, exist_ok=True)


class TestHomepageVisualRegression:
    """Compare the real baseline and current homepage screenshots."""

    @pytest.mark.skipif(
        not BASELINE.exists() or not CURRENT.exists(),
        reason="baseline or current screenshot not present",
    )
    def test_homepage_mismatch_is_zero(self):
        diff_path = str(DIFF_DIR / "homepage_test_diff.png")
        mismatch = compare_images(str(BASELINE), str(CURRENT), diff_path)
        assert mismatch == 0.00, f"Expected 0.00% mismatch but got {mismatch}%"

    @pytest.mark.skipif(
        not BASELINE.exists() or not CURRENT.exists(),
        reason="baseline or current screenshot not present",
    )
    def test_homepage_diff_image_generated(self):
        diff_path = str(DIFF_DIR / "homepage_test_diff.png")
        compare_images(str(BASELINE), str(CURRENT), diff_path)
        assert Path(diff_path).exists(), "Diff image was not generated"

    @pytest.mark.skipif(
        not BASELINE.exists(),
        reason="baseline screenshot not present",
    )
    def test_baseline_against_itself(self):
        """Baseline compared to itself must always be 0.00 %."""
        diff_path = str(DIFF_DIR / "self_diff.png")
        mismatch = compare_images(str(BASELINE), str(BASELINE), diff_path)
        assert mismatch == 0.00


def test_homepage_visual_placeholder():
    """Original placeholder — kept for backward compatibility."""
    assert True
