# LAB03 — Continuous Integration (CI/CD)

## Testing framework
I use **pytest** because it has concise syntax, fixtures, and is the most common modern choice for Python projects.

## What is tested
- `GET /`: JSON structure and required fields
- `GET /health`: status, timestamp, uptime
- `404`: error response is JSON

## CI workflow
Workflow file: `.github/workflows/python-ci.yml`

Triggers:
- push / pull_request when files in `app_python/**` change

Stages:
1) Lint + tests (ruff + pytest)
2) Security scan (Snyk)
3) Docker build & push (only on push to master/main)

## Versioning strategy
I use **CalVer**: `YYYY.MM.DD.<run_number>` plus `latest`.

## Evidence
- Link to a successful workflow run: https://github.com/kvassoedik/DevOps-Core-Course/actions/runs/21948369748
- Docker Hub repo: https://hub.docker.com/repository/docker/kvassoedik/devops-info-service
- Screenshot of local tests: `docs/screenshots/09-local-tests.png`
- Badge in README: added
- Caching: enabled via `actions/setup-python` pip cache
