"""FastAPI service for running visual regression tests."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from src.main.image_compare.comparator import compare_images
from src.main.report_generator.report import generate_report
from src.main.screenshot_capture.capture import capture_screenshot

app = FastAPI(title="Visual Regression Testing API")


class TestRequest(BaseModel):
    """Request payload for triggering a visual regression run."""

    url: str


@app.get("/")
def root() -> dict:
    """Basic service status endpoint."""
    return {"message": "Visual Regression Testing API is running"}


@app.get("/health")
def health_check() -> dict:
    """Health endpoint kept for CI/monitoring compatibility."""
    return {"status": "ok", "service": "visual-regression-testing"}


@app.post("/run-test")
def run_test(request: TestRequest) -> dict:
    """Run visual regression flow for the provided URL."""
    baseline_dir = Path("baseline")
    current_dir = Path("current")
    diff_dir = Path("diff")
    reports_dir = Path("reports")

    # Ensure required folders are available before file operations.
    for directory in (baseline_dir, current_dir, diff_dir, reports_dir):
        directory.mkdir(parents=True, exist_ok=True)

    baseline_path = baseline_dir / "homepage.png"
    current_path = current_dir / "homepage.png"
    diff_path = diff_dir / "homepage_diff.png"

    try:
        # Capture baseline only once if it does not already exist.
        if not baseline_path.exists():
            capture_screenshot(request.url, str(baseline_path))

        # Always capture a fresh current screenshot for comparison.
        capture_screenshot(request.url, str(current_path))
        mismatch_percentage = compare_images(
            str(baseline_path), str(current_path), str(diff_path)
        )
        report_path = generate_report(
            url=request.url,
            baseline=str(baseline_path),
            new=str(current_path),
            diff=str(diff_path),
            mismatch=mismatch_percentage,
        )
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Visual regression run failed: {exc}"
        ) from exc

    return {
        "baseline_image": str(baseline_path),
        "current_image": str(current_path),
        "diff_image": str(diff_path),
        "mismatch_percentage": mismatch_percentage,
        "report": report_path,
    }
