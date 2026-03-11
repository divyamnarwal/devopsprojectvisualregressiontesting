# Visual Regression Testing System

A DevOps-ready application scaffold for capturing website screenshots, comparing them against baselines, detecting visual regressions, and generating test reports.

## Project Overview

This repository provides a clean starter structure for a visual testing platform that can be integrated into CI/CD pipelines. It separates core comparison logic, automation scripts, API endpoints, infrastructure manifests, and monitoring configuration.

## Features

- Screenshot capture module placeholder.
- Image comparison module placeholder.
- Report generation module placeholder.
- FastAPI health endpoint for service readiness checks.
- CI/CD pipeline scaffold using GitHub Actions.
- Containerization with Docker and deployment templates for Kubernetes.
- Monitoring placeholders for Prometheus and Grafana.

## Tech Stack

- Python 3.12
- FastAPI
- Pytest
- Pillow
- Docker
- Kubernetes
- GitHub Actions
- Prometheus + Grafana

## Project Structure

```text
devopsprojectvisualregressiontesting/
├── src/
│   ├── main/
│   │   ├── screenshot_capture/capture.py
│   │   ├── image_compare/comparator.py
│   │   ├── report_generator/report.py
│   │   ├── api/server.py
│   │   └── config/settings.yaml
│   ├── scripts/
│   │   ├── run_visual_tests.sh
│   │   └── generate_report.sh
│   └── test/test_comparator.py
├── docs/
├── infrastructure/
│   ├── docker/Dockerfile
│   └── kubernetes/
├── pipelines/github-actions/cicd.yml
├── monitoring/
├── tests/visual_tests/test_homepage.py
├── presentations/
├── deliverables/
├── requirements.txt
├── .env
├── Dockerfile
└── README.md
```

## CI/CD Readiness

The repository is organized with dedicated directories for pipeline definitions, infrastructure-as-code, monitoring, automated tests, and documentation to support iterative DevOps delivery.

## Running with Docker

Build the Docker image:

```bash
docker build -t visual-regression-system .
```

Run the container:

```bash
docker run -p 8000:8000 visual-regression-system
```
