## ADDED Requirements

### Requirement: Telemetry Ingest
The system SHALL provide a telemetry ingestion capability that accepts device telemetry over MQTT and HTTP, validates payload schema, associates data with a registered device, and persists telemetry to the configured storage backend.

#### Scenario: Device sends valid telemetry via MQTT
- **GIVEN** device `device-123` exists in the device registry
- **WHEN** the device publishes to topic `devices/device-123/telemetry` a JSON payload matching the telemetry schema
- **THEN** the system SHALL validate the payload
- **AND** the system SHALL persist the telemetry record with a server-received timestamp and the device id
- **AND** the system SHALL return an acknowledgement to the broker (QoS 1/2 semantics remain handled by MQTT broker)

#### Scenario: Device sends valid telemetry via HTTP
- **GIVEN** device `device-123` exists and provides valid credentials if auth is enabled
- **WHEN** the device sends a POST to `/v1/devices/device-123/telemetry` with a JSON payload matching the telemetry schema
- **THEN** the system SHALL validate the payload
- **AND** the system SHALL respond HTTP 200 with a JSON acknowledgement
- **AND** the telemetry SHALL be persisted to the configured backend

#### Scenario: Telemetry with invalid schema
- **GIVEN** a device publishes telemetry with missing required fields or invalid types
- **WHEN** the payload is received
- **THEN** the system SHALL reject the payload and log a validation error
- **AND** the system SHALL return HTTP 400 for HTTP ingestion, or drop/park the message for MQTT ingestion depending on configuration

#### Scenario: Out-of-window timestamp
- **GIVEN** a telemetry payload contains a timestamp outside the configured allowed skew (e.g., > 24 hours in the past or future)
- **WHEN** the payload is validated
- **THEN** the system SHALL accept the payload but annotate it as `timestamp_normalized: true` and store both original and normalized times

#### Scenario: Device unknown
- **GIVEN** telemetry is received for `device-unknown` which is not in the device registry
- **WHEN** the payload is received
- **THEN** the system SHALL reject the telemetry and emit an alert or log entry for operator review

### Requirement: Telemetry Schema
The telemetry payload SHALL be JSON and SHALL include at least the following fields:
- `device_id`: string (device identifier)
- `timestamp`: ISO-8601 string / unix epoch (server normalizes)
- `metrics`: object (key-value map of measured metrics, e.g., `{"temp_c": 22.5}`)

#### Scenario: Minimal telemetry example
- **WHEN** device publishes:

```json
{
  "device_id": "device-123",
  "timestamp": "2025-11-04T12:00:00Z",
  "metrics": {"temp_c": 22.5, "humidity_pct": 45}
}
```

- **THEN** the system SHALL persist the metrics and index by device and time for queries
