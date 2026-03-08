#!/usr/bin/env bash
set -euo pipefail

# Purpose: run visual regression test flow in local/CI environments.
echo "Running visual regression tests..."
# TODO: Trigger screenshot capture + image comparison pipeline.
# Placeholder command:
pytest -q tests/visual_tests
