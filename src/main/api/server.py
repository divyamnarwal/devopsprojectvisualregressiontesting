"""API server module.

Purpose:
- Expose service endpoints for health checks and future test orchestration.
"""

from fastapi import FastAPI

app = FastAPI(title="Visual Regression Testing System")


@app.get("/health")
def health_check() -> dict:
    """Service health endpoint used by monitoring and readiness checks."""
    return {"status": "ok", "service": "visual-regression-testing"}
