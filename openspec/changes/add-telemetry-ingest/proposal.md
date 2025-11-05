# Change: add-telemetry-ingest

## Why
Provide a standard, validated telemetry ingestion pipeline for devices so telemetry can be reliably accepted, persisted, and queried. This enables downstream analytics, grading scenarios, and device monitoring in the course homework environment.

## What Changes
- ADDED: A telemetry ingest capability that accepts MQTT and HTTP telemetry payloads, validates schema, associates data with a device registry entry, and persists to the timeseries store.
- ADDED: A minimal device registry integration for mapping device IDs to metadata and credentials.
- ADDED: Acceptance tests and a small device simulator for end-to-end verification.

**BREAKING:** None.

## Impact
- Affected specs: `device` (new telemetry requirements)
- Affected code: ingestion service (MQTT client, HTTP endpoint), storage adapter, and device registry code paths
- Operational: Requires a running MQTT broker and a timeseries-capable persistence backend (InfluxDB/TimescaleDB/Postgres). For local testing, SQLite fallback allowed.
