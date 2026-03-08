"""HTML report generator for visual regression results."""

from __future__ import annotations

from pathlib import Path


def _image_path_for_report(image_path: str) -> str:
    """Return a path suitable for HTML rendered from reports/report.html."""
    path = Path(image_path)
    if path.is_absolute():
        try:
            path = path.relative_to(Path.cwd())
        except ValueError:
            return path.as_posix()
    if path.parts and path.parts[0] == "..":
        return path.as_posix()
    return (Path("..") / path).as_posix()


def generate_report(
    url: str, baseline: str, new: str, diff: str, mismatch: float
) -> str:
    """Generate a simple HTML report and save it to ``reports/report.html``."""
    reports_dir = Path("reports")
    reports_dir.mkdir(parents=True, exist_ok=True)
    report_path = reports_dir / "report.html"

    baseline_html = _image_path_for_report(baseline)
    new_html = _image_path_for_report(new)
    diff_html = _image_path_for_report(diff)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Visual Regression Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; color: #222; }}
    h1 {{ margin-bottom: 8px; }}
    .meta {{ margin-bottom: 20px; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 16px; }}
    .card {{ border: 1px solid #ddd; border-radius: 8px; padding: 12px; }}
    img {{ width: 100%; border-radius: 6px; border: 1px solid #eee; }}
  </style>
</head>
<body>
  <h1>Visual Regression Report</h1>
  <div class="meta">
    <p><strong>URL Tested:</strong> {url}</p>
    <p><strong>Mismatch Percentage:</strong> {mismatch:.2f}%</p>
  </div>
  <div class="grid">
    <div class="card">
      <h2>Baseline</h2>
      <img src="{baseline_html}" alt="Baseline screenshot" />
    </div>
    <div class="card">
      <h2>New Screenshot</h2>
      <img src="{new_html}" alt="New screenshot" />
    </div>
    <div class="card">
      <h2>Diff Image</h2>
      <img src="{diff_html}" alt="Diff image" />
    </div>
  </div>
</body>
</html>
"""

    report_path.write_text(html, encoding="utf-8")
    return str(report_path)
