"""Tests for the HTML report generator."""

from __future__ import annotations

from pathlib import Path

from src.main.report_generator.report import generate_report, _image_path_for_report


class TestGenerateReport:
    """The report generator must produce a valid HTML file with correct data."""

    def test_report_file_created(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        path = generate_report("https://example.com", "baseline/a.png",
                               "current/a.png", "diff/a.png", 0.00)
        assert Path(path).exists()

    def test_report_contains_url(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        url = "https://example.com"
        path = generate_report(url, "b.png", "c.png", "d.png", 0.00)
        content = Path(path).read_text(encoding="utf-8")
        assert url in content

    def test_report_contains_mismatch_value(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        path = generate_report("https://example.com", "b.png", "c.png",
                               "d.png", 3.14)
        content = Path(path).read_text(encoding="utf-8")
        assert "3.14%" in content

    def test_report_contains_zero_mismatch(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        path = generate_report("https://example.com", "b.png", "c.png",
                               "d.png", 0.00)
        content = Path(path).read_text(encoding="utf-8")
        assert "0.00%" in content

    def test_report_is_valid_html(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        path = generate_report("https://example.com", "b.png", "c.png",
                               "d.png", 0.00)
        content = Path(path).read_text(encoding="utf-8")
        assert content.startswith("<!DOCTYPE html>")
        assert "</html>" in content

    def test_report_contains_image_references(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        path = generate_report("https://example.com",
                               "baseline/shot.png", "current/shot.png",
                               "diff/shot.png", 0.00)
        content = Path(path).read_text(encoding="utf-8")
        assert "shot.png" in content


class TestImagePathForReport:
    """Helper that adjusts image paths for the HTML report location."""

    def test_relative_path(self):
        result = _image_path_for_report("baseline/img.png")
        assert result == "../baseline/img.png"

    def test_already_prefixed(self):
        result = _image_path_for_report("../baseline/img.png")
        assert result == "../baseline/img.png"
