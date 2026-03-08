"""Image comparison engine built with OpenCV."""

from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


def compare_images(baseline_path: str, new_path: str, diff_path: str) -> float:
    """Compare two images, write a highlighted diff image, and return mismatch %."""
    baseline_image = cv2.imread(baseline_path)
    new_image = cv2.imread(new_path)

    if baseline_image is None:
        raise FileNotFoundError(f"Baseline image not found: {baseline_path}")
    if new_image is None:
        raise FileNotFoundError(f"New image not found: {new_path}")

    if baseline_image.shape != new_image.shape:
        # Keep comparison possible even if screenshot sizes differ.
        new_image = cv2.resize(
            new_image, (baseline_image.shape[1], baseline_image.shape[0])
        )

    baseline_gray = cv2.cvtColor(baseline_image, cv2.COLOR_BGR2GRAY)
    new_gray = cv2.cvtColor(new_image, cv2.COLOR_BGR2GRAY)

    absolute_diff = cv2.absdiff(baseline_gray, new_gray)
    _, threshold = cv2.threshold(absolute_diff, 30, 255, cv2.THRESH_BINARY)

    changed_pixels = int(np.count_nonzero(threshold))
    total_pixels = threshold.shape[0] * threshold.shape[1]
    mismatch_percentage = (changed_pixels / total_pixels) * 100

    diff_highlight = new_image.copy()
    contours, _ = cv2.findContours(
        threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )
    for contour in contours:
        # Ignore tiny noise blocks to keep the diff image readable.
        if cv2.contourArea(contour) < 40:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cv2.rectangle(diff_highlight, (x, y), (x + w, y + h), (0, 0, 255), 2)

    diff_output = Path(diff_path)
    diff_output.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(diff_output), diff_highlight)

    return round(float(mismatch_percentage), 2)
