"""Tests for the FastAPI health endpoint."""

from __future__ import annotations

from fastapi.testclient import TestClient

from src.main.api.server import app

client = TestClient(app)


def test_health_returns_ok():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["service"] == "visual-regression-testing"


def test_health_response_keys():
    resp = client.get("/health")
    assert set(resp.json().keys()) == {"status", "service"}
