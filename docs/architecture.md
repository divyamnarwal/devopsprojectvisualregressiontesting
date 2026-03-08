# Architecture

This document outlines the high-level architecture for the Visual Regression Testing System.

- Screenshot capture service collects fresh UI snapshots.
- Image comparison engine checks differences against baselines.
- Report generator produces test artifacts for CI/CD and teams.
- API layer exposes health and orchestration endpoints.
