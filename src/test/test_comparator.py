"""Tests for the image comparison engine."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np
import pytest

from src.main.image_compare.comparator import compare_images


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _create_solid_image(path: str, color: tuple, width: int = 100, height: int = 80):
    """Create a solid-colour BGR image and save it to *path*."""
    img = np.full((height, width, 3), color, dtype=np.uint8)
    cv2.imwrite(path, img)


def _create_image_with_block(path: str, bg: tuple, block_color: tuple,
                             width: int = 100, height: int = 80):
    """Create an image with a coloured block in the centre."""
    img = np.full((height, width, 3), bg, dtype=np.uint8)
    x1, y1 = width // 4, height // 4
    x2, y2 = 3 * width // 4, 3 * height // 4
    img[y1:y2, x1:x2] = block_color
    cv2.imwrite(path, img)


# ---------------------------------------------------------------------------
# Tests – identical images
# ---------------------------------------------------------------------------

class TestIdenticalImages:
    """Comparing an image to itself must always report 0.00 % mismatch."""

    def test_solid_white_identical(self, tmp_path):
        baseline = str(tmp_path / "white_a.png")
        copy = str(tmp_path / "white_b.png")
        diff = str(tmp_path / "diff.png")
        _create_solid_image(baseline, (255, 255, 255))
        _create_solid_image(copy, (255, 255, 255))
        assert compare_images(baseline, copy, diff) == 0.00

    def test_solid_black_identical(self, tmp_path):
        baseline = str(tmp_path / "black_a.png")
        copy = str(tmp_path / "black_b.png")
        diff = str(tmp_path / "diff.png")
        _create_solid_image(baseline, (0, 0, 0))
        _create_solid_image(copy, (0, 0, 0))
        assert compare_images(baseline, copy, diff) == 0.00

    def test_coloured_identical(self, tmp_path):
        baseline = str(tmp_path / "colour_a.png")
        copy = str(tmp_path / "colour_b.png")
        diff = str(tmp_path / "diff.png")
        _create_solid_image(baseline, (42, 128, 200))
        _create_solid_image(copy, (42, 128, 200))
        assert compare_images(baseline, copy, diff) == 0.00

    def test_patterned_identical(self, tmp_path):
        baseline = str(tmp_path / "pattern_a.png")
        copy = str(tmp_path / "pattern_b.png")
        diff = str(tmp_path / "diff.png")
        _create_image_with_block(baseline, (255, 255, 255), (0, 0, 255))
        _create_image_with_block(copy, (255, 255, 255), (0, 0, 255))
        assert compare_images(baseline, copy, diff) == 0.00

    def test_same_file_as_both_inputs(self, tmp_path):
        img = str(tmp_path / "single.png")
        diff = str(tmp_path / "diff.png")
        _create_solid_image(img, (100, 150, 200))
        assert compare_images(img, img, diff) == 0.00


# ---------------------------------------------------------------------------
# Tests – different images
# ---------------------------------------------------------------------------

class TestDifferentImages:
    """When images differ the mismatch % must be greater than zero."""

    def test_white_vs_black(self, tmp_path):
        a = str(tmp_path / "white.png")
        b = str(tmp_path / "black.png")
        diff = str(tmp_path / "diff.png")
        _create_solid_image(a, (255, 255, 255))
        _create_solid_image(b, (0, 0, 0))
        mismatch = compare_images(a, b, diff)
        assert mismatch > 0
        assert mismatch == 100.0  # completely different in grayscale

    def test_partial_change(self, tmp_path):
        a = str(tmp_path / "a.png")
        b = str(tmp_path / "b.png")
        diff = str(tmp_path / "diff.png")
        _create_solid_image(a, (255, 255, 255))
        _create_image_with_block(b, (255, 255, 255), (0, 0, 0))
        mismatch = compare_images(a, b, diff)
        assert 0 < mismatch < 100

    def test_subtle_change_below_threshold(self, tmp_path):
        """A tiny intensity shift (<=30) should remain under the binary threshold."""
        a = str(tmp_path / "a.png")
        b = str(tmp_path / "b.png")
        diff = str(tmp_path / "diff.png")
        _create_solid_image(a, (128, 128, 128))
        _create_solid_image(b, (130, 130, 130))  # within threshold
        assert compare_images(a, b, diff) == 0.00


# ---------------------------------------------------------------------------
# Tests – diff image output
# ---------------------------------------------------------------------------

class TestDiffOutput:
    """The comparator must write a readable diff image to disk."""

    def test_diff_image_created(self, tmp_path):
        a = str(tmp_path / "a.png")
        b = str(tmp_path / "b.png")
        diff = str(tmp_path / "diff.png")
        _create_solid_image(a, (255, 255, 255))
        _create_solid_image(b, (255, 255, 255))
        compare_images(a, b, diff)
        assert Path(diff).exists()

    def test_diff_image_correct_dimensions(self, tmp_path):
        a = str(tmp_path / "a.png")
        b = str(tmp_path / "b.png")
        diff = str(tmp_path / "diff.png")
        _create_solid_image(a, (255, 255, 255), width=200, height=150)
        _create_solid_image(b, (255, 255, 255), width=200, height=150)
        compare_images(a, b, diff)
        diff_img = cv2.imread(diff)
        assert diff_img.shape[:2] == (150, 200)

    def test_diff_in_subdirectory(self, tmp_path):
        a = str(tmp_path / "a.png")
        b = str(tmp_path / "b.png")
        diff = str(tmp_path / "sub" / "deep" / "diff.png")
        _create_solid_image(a, (255, 255, 255))
        _create_solid_image(b, (255, 255, 255))
        compare_images(a, b, diff)
        assert Path(diff).exists()


# ---------------------------------------------------------------------------
# Tests – dimension mismatch (resize logic)
# ---------------------------------------------------------------------------

class TestDimensionMismatch:
    """Images of different sizes should still compare without errors."""

    def test_resize_keeps_zero_mismatch_for_same_colour(self, tmp_path):
        a = str(tmp_path / "a.png")
        b = str(tmp_path / "b.png")
        diff = str(tmp_path / "diff.png")
        _create_solid_image(a, (128, 128, 128), width=100, height=80)
        _create_solid_image(b, (128, 128, 128), width=200, height=160)
        assert compare_images(a, b, diff) == 0.00

    def test_resize_detects_difference(self, tmp_path):
        a = str(tmp_path / "a.png")
        b = str(tmp_path / "b.png")
        diff = str(tmp_path / "diff.png")
        _create_solid_image(a, (255, 255, 255), width=100, height=80)
        _create_solid_image(b, (0, 0, 0), width=200, height=160)
        assert compare_images(a, b, diff) > 0


# ---------------------------------------------------------------------------
# Tests – error handling
# ---------------------------------------------------------------------------

class TestErrorHandling:
    """Missing input files must raise clear errors."""

    def test_missing_baseline_raises(self, tmp_path):
        b = str(tmp_path / "b.png")
        diff = str(tmp_path / "diff.png")
        _create_solid_image(b, (255, 255, 255))
        with pytest.raises(FileNotFoundError):
            compare_images(str(tmp_path / "nope.png"), b, diff)

    def test_missing_new_image_raises(self, tmp_path):
        a = str(tmp_path / "a.png")
        diff = str(tmp_path / "diff.png")
        _create_solid_image(a, (255, 255, 255))
        with pytest.raises(FileNotFoundError):
            compare_images(a, str(tmp_path / "nope.png"), diff)


# ---------------------------------------------------------------------------
# Tests – original placeholder (kept for compatibility)
# ---------------------------------------------------------------------------

def test_compare_images_placeholder():
    assert callable(compare_images)
