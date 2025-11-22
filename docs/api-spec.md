# API Specification

## Authentication

### POST /auth/login

Authenticate a user and receive JWT token.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "jwt_token_string",
  "token_type": "bearer",
  "user": {
    "id": "1",
    "email": "user@example.com",
    "role": "admin"
  }
}
```

## Events

### POST /events

Create a new event from EventSpec.

**Request Body:** Full EventSpec JSON (see schemas/event_spec.json)

**Response:**
```json
{
  "event_id": "uuid",
  "status": "created"
}
```

### GET /events/{event_id}

Get event by ID.

**Response:**
```json
{
  "event": { ...full EventSpec... }
}
```

### GET /events

List events with pagination.

**Query Parameters:**
- `page` (default: 1)
- `limit` (default: 20, max: 100)
- `search` (optional)

**Response:**
```json
{
  "events": [...],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 50,
    "pages": 3
  }
}
```

## Plan Generation

### POST /plan-event

Generate an EventPlan from EventSpec.

**Request Body:** EventSpec JSON

**Query Parameters:**
- `event_id` (optional) - Use existing event

**Response:** Full EventPlan JSON (see schemas/event_plan.json)

### GET /plan-event/{event_id}

Get latest plan for an event.

**Response:**
```json
{
  "event_plan": { ...EventPlan... }
}
```

## Ingestion

### POST /ingest/inventory

Upload Current RMS products CSV.

**Request:** multipart/form-data with CSV file

**Response:**
```json
{
  "products_ingested": 324,
  "embeddings_generated": 324
}
```

### POST /ingest/stock-levels

Upload stock levels CSV.

### POST /ingest/historic-events

Upload historic events JSON.

**Request Body:**
```json
{
  "events": [
    {
      "title": "Event Name",
      "body": "Full description..."
    }
  ]
}
```

### POST /ingest/templates

Upload SOP templates.

**Request Body:**
```json
{
  "templates": [
    {
      "title": "Template Name",
      "doc_type": "sop",
      "body": "Template content..."
    }
  ]
}
```

## Exports

### GET /export/equipment-csv/{event_id}

Download equipment CSV.

### GET /export/crew-csv/{event_id}

Download crew CSV.

### GET /export/summary/{event_id}

Download plan summary as text.

## Admin

### POST /admin/rebuild-embeddings

Rebuild all embeddings (admin only).

**Response:**
```json
{
  "products_rebuilt": 100,
  "events_rebuilt": 50,
  "templates_rebuilt": 20
}
```

## Health

### GET /health

Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "lunaverse-show-brain"
}
```

