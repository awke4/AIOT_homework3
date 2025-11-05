# Project Context

## Purpose
This repository contains the course/homework project for AIoT (HW3): an IoT/edge+cloud exercise that demonstrates device telemetry ingestion, device management, and basic analytics. The project is intended as a small, reproducible platform to: collect telemetry from constrained devices, persist and query timeseries data, and expose management and visualization endpoints for instructors and graders.

Notes / assumptions: I inferred the AIoT purpose from the workspace name (`AIOT/hw3`). If this is a different project goal (e.g., industrial IoT, simulation), tell me and I'll adapt this section.

## Tech Stack (recommended / assumed)
- Language: Python 3.10+ (preferred for quick IoT prototypes) — alternative: Node.js
- Server / API: FastAPI (async, small, easy to test)
- Messaging / Device transport: MQTT (e.g., Mosquitto) for device-to-cloud telemetry; HTTP/HTTPS for management/control
- Storage:
	- Time-series: InfluxDB or PostgreSQL (timescale) for persisted telemetry (optional for HW; SQLite acceptable for local tests)
	- Metadata: PostgreSQL or SQLite for device registry
- Local dev / container: Docker + docker-compose
- Testing: pytest
- Linting / formatting: black, isort, flake8 (or ruff)
- CI: GitHub Actions (workflows for lint/test/build)

If you prefer a different stack (Node/TypeScript, Go, etc.), tell me and I will rewrite the conventions and templates accordingly.

## Project Conventions

### Code Style
- Python projects should use Black for formatting and ruff/flake8 for linting. Use type hints (mypy optional but encouraged).
- Small modules (<= 300 lines) preferred. Keep functions single-responsibility and well-documented.
- File and directory names: kebab-case for openspec content and change IDs; snake_case for Python modules; PascalCase for classes.

### Architecture Patterns
- Clear separation between device-facing ingestion (MQTT/HTTP), business logic (ingest validation, enrichment), persistence layers, and API surface.
- Keep device simulator/test helpers separate from production code (e.g., `tools/device_simulator/`).
- Prefer small, focused capabilities under `openspec/specs/<capability>/`.

### Testing Strategy
- Unit tests: pytest for individual modules with mocks for external dependencies (MQTT broker, DB).
- Integration tests: run a lightweight end-to-end scenario using a local broker (e.g., eclipse-mosquitto) and a temporary DB (SQLite or dockerized Postgres).
- Keep tests fast (< 2s per unit test) and deterministic. CI should run full test matrix.

### Git Workflow
- Branching: `main` (protected) and feature branches `feature/<short-desc>` or `change/<change-id>` for OpenSpec changes.
- Commits: conventional-ish messages, prefix with the change-id when implementing a proposal (e.g., `add-telemetry-ingest: implement validation`).
- PRs: open draft PR for early review; link the OpenSpec change directory in the PR description.

## Domain Context
- Devices are resource-constrained, connect intermittently, and send small JSON telemetry payloads over MQTT.
- Telemetry packets should be validated server-side (schema, timestamps, device id).
- Device identity is managed via a device registry (device id, metadata, credentials/keys).

## Important Constraints
- Devices may experience clock drift; server should accept timestamps within a configurable window and normalize when necessary.
- Network connectivity is unreliable; ingestion must be resilient and idempotent.
- For homework/demo purposes, privacy/security requirements are minimal, but production changes must include authentication, encryption, and secrets management.

## External Dependencies
- MQTT broker (local dev: eclipse-mosquitto container)
- Optional: InfluxDB / TimescaleDB / PostgreSQL for telemetry storage
- Optional: Cloud services for authentication or analytics (AWS IoT Core, GCP Pub/Sub) — explicitly list if you plan to use one

---

If you'd like, I can adapt these specifics to your preferred stack (Node/Python/Go), or I can detect the actual code in the repo and rewrite the file to exactly match the project's packages and tooling. Tell me which direction you prefer.
