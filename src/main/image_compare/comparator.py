"""Image comparison module.

Purpose:
- Compare baseline and candidate screenshots and return difference metadata.
"""


def compare_images(baseline_path: str, candidate_path: str) -> dict:
    """Compare two images and return a simple result payload."""
    # Placeholder logic for bootstrap stage.
    # TODO: Implement SSIM/perceptual diff with mismatch threshold handling.
    _ = (baseline_path, candidate_path)
    return {"match": True, "difference_score": 0.0, "diff_image": None}
