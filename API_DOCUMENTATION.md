# 📡 API Documentation

Complete REST API documentation for the SDN AI Backend.

## Base URL

```
http://localhost:5000
```

## Authentication

Currently, no authentication is required. For production, consider implementing:
- JWT tokens
- API keys
- OAuth 2.0

## Response Format

All responses use JSON format with consistent structure:

```json
{
  "success": true,
  "data": {},
  "error": null,
  "timestamp": "2026-05-17T10:30:00Z"
}
```

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK - Request successful |
| 400 | Bad Request - Invalid parameters |
| 404 | Not Found - Endpoint not found |
| 500 | Server Error - Internal error |
| 503 | Service Unavailable - Model not loaded |

## Endpoints

### 1. Health Check

Check backend health and system status.

**Endpoint:** `GET /health`

**Description:** Returns server status, uptime, and system information.

**Parameters:** None

**Response:**
```json
{
  "status": "ok",
  "timestamp": "2026-05-17T10:30:00Z",
  "uptime": "2h 15m",
  "version": "1.0.0",
  "models_cached": 1,
  "requests_processed": 150
}
```

**Status:** `200 OK`

**cURL Example:**
```bash
curl -X GET http://localhost:5000/health
```

**Python Example:**
```python
import requests

response = requests.get('http://localhost:5000/health')
data = response.json()
print(f"Status: {data['status']}")
print(f"Uptime: {data['uptime']}")
```

---

### 2. Predict Congestion

Predict congestion probability for a network link.

**Endpoint:** `POST /api/predict`

**Description:** Uses LSTM model to predict congestion probability for given link features.

**Request Body:**
```json
{
  "link_id": "s1-s3",
  "features": [
    0.75,    // Bandwidth usage (0-1)
    12.3,    // RTT (ms)
    0.02,    // Packet drop rate (0-1)
    45.6,    // Queue length (packets)
    0.8      // Inter-arrival time (ms)
  ]
}
```

**Parameters:**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| link_id | string | No | Link identifier (e.g., "s1-s3") |
| features | array | Yes | Feature vector [bandwidth, RTT, drop_rate, queue, inter_arrival] |

**Response:**
```json
{
  "success": true,
  "link_id": "s1-s3",
  "probability": 0.872,
  "risk_level": "HIGH",
  "threshold": 0.7,
  "congested": true,
  "timestamp": "2026-05-17T10:30:00Z",
  "model_version": "v1.0"
}
```

**Response Fields:**

| Field | Type | Description |
|-------|------|-------------|
| success | boolean | Operation success status |
| link_id | string | Echo of requested link ID |
| probability | float | Congestion probability (0-1) |
| risk_level | string | Risk classification (LOW/MEDIUM/HIGH/CRITICAL) |
| threshold | float | Congestion decision threshold |
| congested | boolean | Whether link is congested |
| timestamp | string | ISO 8601 timestamp |
| model_version | string | Model version used |

**Status:** `200 OK` (success), `400 Bad Request` (invalid input), `503 Service Unavailable` (model error)

**Error Response:**
```json
{
  "error": "Features must be a list",
  "type": "validation_error"
}
```

**cURL Example:**
```bash
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{
    "link_id": "s1-s3",
    "features": [0.75, 12.3, 0.02, 45.6, 0.8]
  }'
```

**Python Example:**
```python
import requests

data = {
    "link_id": "s1-s3",
    "features": [0.75, 12.3, 0.02, 45.6, 0.8]
}

response = requests.post(
    'http://localhost:5000/api/predict',
    json=data
)

result = response.json()
print(f"Congestion: {result['probability']:.2%}")
print(f"Risk Level: {result['risk_level']}")
```

**Risk Level Classification:**

| Level | Probability Range | Action |
|-------|-------------------|--------|
| LOW | < 40% | No action needed |
| MEDIUM | 40-60% | Monitor closely |
| HIGH | 60-80% | Prepare mitigation |
| CRITICAL | > 80% | Activate rerouting |

---

### 3. Get Statistics

Get current system and API statistics.

**Endpoint:** `GET /api/stats`

**Description:** Returns backend statistics, metrics, and configuration.

**Parameters:** None

**Response:**
```json
{
  "success": true,
  "requests_total": 450,
  "models_cached": 1,
  "uptime_seconds": 7920,
  "timestamp": "2026-05-17T10:30:00Z",
  "config": {
    "log_level": "INFO",
    "lstm_input_shape": 5,
    "congestion_threshold": 0.7
  }
}
```

**Status:** `200 OK`

**cURL Example:**
```bash
curl http://localhost:5000/api/stats
```

**Python Example:**
```python
import requests

response = requests.get('http://localhost:5000/api/stats')
stats = response.json()

print(f"Total Requests: {stats['requests_total']}")
print(f"Uptime: {stats['uptime_seconds']/3600:.1f} hours")
```

---

### 4. Get Configuration

Get current system configuration (safe values only).

**Endpoint:** `GET /api/config`

**Description:** Returns non-sensitive configuration values.

**Parameters:** None

**Response:**
```json
{
  "success": true,
  "config": {
    "flask_env": "production",
    "log_level": "INFO",
    "lstm_config": {
      "input_shape": 5,
      "hidden_units": 128,
      "layers": 2
    },
    "dqn_config": {
      "state_size": 10,
      "action_size": 8,
      "learning_rate": 0.001
    },
    "thresholds": {
      "congestion": 0.7,
      "bandwidth_warning": 80,
      "packet_drop": 5
    },
    "feature_scaling": "minmax"
  }
}
```

**Status:** `200 OK`

**cURL Example:**
```bash
curl http://localhost:5000/api/config
```

---

## Error Handling

### Common Errors

**400 Bad Request - Missing Features**
```json
{
  "error": "Missing 'features' field",
  "required_fields": ["link_id", "features"],
  "type": "validation_error"
}
```

**400 Bad Request - Invalid Features**
```json
{
  "error": "Features must be a list",
  "type": "validation_error"
}
```

**503 Service Unavailable - Model Not Loaded**
```json
{
  "error": "Model not available",
  "suggestion": "Ensure model is trained and at correct path",
  "type": "model_error"
}
```

**500 Internal Server Error**
```json
{
  "error": "Internal server error",
  "type": "server_error",
  "message": "Detailed error message (only in debug mode)"
}
```

### Error Response Structure

```json
{
  "error": "Description of error",
  "type": "error_type",
  "message": "Additional details (optional)"
}
```

---

## Rate Limiting

Currently no rate limiting is implemented. For production, consider:

- Implement token bucket algorithm
- Limit requests per IP: 100 req/min
- Limit requests per user: 1000 req/hour

Example headers (future):
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1620000000
```

---

## Pagination

Not currently implemented. Future endpoints returning lists will use:

```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "pages": 8
  }
}
```

---

## Request/Response Examples

### Batch Predictions

```python
import requests

predictions = []
links = [
    {"link_id": "s1-s2", "features": [0.6, 10.5, 0.01, 30.2, 0.7]},
    {"link_id": "s2-s3", "features": [0.8, 15.3, 0.05, 50.1, 0.9]},
    {"link_id": "s3-s4", "features": [0.4, 8.2, 0.00, 20.5, 0.5]},
]

for link_data in links:
    response = requests.post(
        'http://localhost:5000/api/predict',
        json=link_data
    )
    predictions.append(response.json())

# Process results
congested_links = [p for p in predictions if p['congested']]
print(f"Congested links: {len(congested_links)}")
```

### Real-time Monitoring Loop

```python
import requests
import time
from datetime import datetime

def monitor_network(interval=5):
    """Monitor network links continuously."""
    
    while True:
        try:
            stats = requests.get('http://localhost:5000/api/stats').json()
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] API Stats")
            print(f"  Requests: {stats['requests_total']}")
            print(f"  Uptime: {stats['uptime_seconds']/3600:.1f}h")
            
            time.sleep(interval)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(interval)

if __name__ == "__main__":
    monitor_network()
```

---

## Performance Characteristics

| Operation | Latency | Notes |
|-----------|---------|-------|
| Health Check | < 1ms | Cached response |
| Prediction | 10-50ms | Depends on model size |
| Stats | < 5ms | In-memory data |
| Config | < 1ms | Static data |

---

## Versioning

Current API version: **1.0.0**

Future versions will be available at:
- `/v2/api/predict`
- `/v2/api/stats`

---

## Changelog

### v1.0.0 (2026-05-17)
- Initial API release
- Prediction endpoint
- Health check
- Statistics endpoint
- Configuration endpoint

---

## Support

For API issues and questions:
- Email: adityamaurya@mmmut.ac.in
- GitHub Issues: [Report Issue](https://github.com/aditya5289/AI-based-congestion-control-in-SDN/issues)

---

## License

API documentation is part of the AI-Based Congestion Control in SDN project.
Licensed under the MIT License.
