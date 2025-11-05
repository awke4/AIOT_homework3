## 1. Implementation
- [ ] 1.1 Create device registry model + persistence (SQLite / Postgres adapter)
- [ ] 1.2 Implement telemetry ingestion component:
  - [ ] MQTT subscriber that accepts telemetry topic `devices/{device_id}/telemetry`
  - [ ] HTTP POST `/v1/devices/{device_id}/telemetry` endpoint (for constrained devices that use HTTP)
  - [ ] Schema validation and enrichment (timestamps normalization)
- [ ] 1.3 Implement storage adapter (InfluxDB/Postgres/SQLite fallback)
- [ ] 1.4 Add unit tests for validation and persistence
- [ ] 1.5 Add an integration test using a local broker and in-memory DB
- [ ] 1.6 Add device simulator script for demo

## 2. Documentation
- [ ] 2.1 Document telemetry schema and ingestion contract in `openspec/specs/device/spec.md`
- [ ] 2.2 Add quickstart instructions for local dev (docker-compose)

## 3. Optional
- [ ] 3.1 Add metrics and tracing hooks
- [ ] 3.2 Add auth (device credential verification)
