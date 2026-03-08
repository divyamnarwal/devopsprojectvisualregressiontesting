"""Simple visual regression test runner.

This script connects screenshot capture, image comparison, and report generation.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from src.main.image_compare.comparator import compare_images
from src.main.report_generator.report import generate_report
from src.main.screenshot_capture.capture import capture_screenshot


DEFAULT_URL = "https://example.com"


def run_visual_test(url: str = DEFAULT_URL) -> None:
    """Run a single visual regression flow for the given URL."""
    baseline_dir = Path("baseline")
    current_dir = Path("current")
    diff_dir = Path("diff")
    reports_dir = Path("reports")

    # Ensure required directories always exist.
    for directory in (baseline_dir, current_dir, diff_dir, reports_dir):
        directory.mkdir(parents=True, exist_ok=True)

    baseline_path = baseline_dir / "homepage.png"
    current_path = current_dir / "homepage.png"
    diff_path = diff_dir / "homepage_diff.png"

    # First run: create baseline and stop.
    if not baseline_path.exists():
        capture_screenshot(url, str(baseline_path))
        print(f"Baseline created: {baseline_path}")
        return

    # Subsequent runs: capture current screenshot, compare, and report.
    capture_screenshot(url, str(current_path))
    mismatch = compare_images(str(baseline_path), str(current_path), str(diff_path))
    report_file = generate_report(
        url=url,
        baseline=str(baseline_path),
        new=str(current_path),
        diff=str(diff_path),
        mismatch=mismatch,
    )

    print(f"Mismatch percentage: {mismatch:.2f}%")
    print(f"Report generated: {report_file}")


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Run visual regression test.")
    parser.add_argument(
        "url",
        nargs="?",
        default=DEFAULT_URL,
        help=f"Target URL to test (default: {DEFAULT_URL})",
    )
    args = parser.parse_args()
    run_visual_test(args.url)


if __name__ == "__main__":
    main()
