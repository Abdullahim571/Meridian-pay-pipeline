# Meridian-pay-pipeline
Secure CI/CD pipeline demonstration

## Layout

```
.github/workflows/ci.yml   # CI/CD pipeline
app/__init__.py            # Flask app factory
app/wsgi.py                # WSGI entrypoint (gunicorn)
tests/test_app.py          # pytest unit tests
Dockerfile                 # non-root python:3.12-slim image
requirements.txt           # runtime deps
requirements-dev.txt       # test deps
```

## Pipeline

1. **test** – installs deps, runs `pytest` with coverage, uploads JUnit/coverage reports.
2. **build-scan-sign** – builds the image, then:
   - **Trivy** scans it; results go to the Security tab, and the job fails on fixable HIGH/CRITICAL vulns.
   - **Syft** generates an SPDX SBOM (uploaded as a workflow artifact).
   - On `main` (not PRs): pushes to `ghcr.io`, signs the image keylessly with **Cosign**, and attaches the SBOM as a signed attestation.

## Run locally

```bash
pip install -r requirements-dev.txt
pytest
docker build -t meridian-pay . && docker run -p 8000:8000 meridian-pay
```

## Verify a published image

```bash
cosign verify ghcr.io/abdullahim571/meridian-pay-pipeline:latest \
  --certificate-identity https://github.com/Abdullahim571/Meridian-pay-pipeline/.github/workflows/ci.yml@refs/heads/main \
  --certificate-oidc-issuer https://token.actions.githubusercontent.com
```
