
LUNAVERSE SHOW BRAIN v1

FULL MASTER DOCUMENT 

(Project Scope + Developer Handoff + Architecture + Schemas + DB Models + Data Relations + Prompts + UI Spec + API Spec)

⸻

PART 1 — PROJECT OVERVIEW + OBJECTIVES + REQUIREMENTS + COMPLETE PROJECT SCOPE

⸻

1. Project Name & Owner

Project Name: Lunaverse Show Brain v1
Owner: Javad / Lunaverse / Legion AVS
Hosting Environment: Self-hosted Ubuntu server (“lunaverse”), with Dockerized microservices.
Intended Users: TPMs, PMs, TDs, Warehouse & Logistics Managers.

⸻

2. High-Level Description

Lunaverse Show Brain v1 is a private, server-hosted event-production planning engine that transforms structured event inputs into full AI-generated:
	•	Equipment pull lists (mapped to real inventory)
	•	Crew plans (roles, quantities, hours)
	•	Trucking/weight/cube estimations
	•	Optional cost estimates
	•	CSV export for Current RMS & Google Sheets
	•	Historical comparison to prior events
	•	SOP-driven standardization

The system uses:
	•	A Hugging Face LLM (Llama 3 or similar) via paid HF Inference Endpoint
	•	A vector database (Chroma or Qdrant) containing:
	•	Current RMS inventory
	•	Historic show plans
	•	SOPs
	•	FastAPI backend with strict schemas
	•	Browser-based front-end for user interaction
	•	Dockerized infrastructure for reproducibility

All data stays fully private on your Lunaverse Ubuntu server.

⸻

3. Core Idea

“Give me your event spec → receive equipment, crew, trucking, and assumptions instantly.”

This turns hours of manual PM/TD planning into a 15–20 second automated draft.

⸻

4. Project Goals

4.1 Primary Objectives
	1.	Reduce planning time per event by 40–60%.
	2.	Standardize show plans using “gold standard” show templates.
	3.	Use real Current RMS inventory for accurate item selection.
	4.	Build a reusable AI engine that can be commercialized as:
	•	SaaS
	•	White-label solution
	•	Private AI consultant tool for other AV firms.
	5.	Keep all data local & secure.

4.2 Secondary Objectives
	1.	Create a modular architecture ready for multi-tenant v2.
	2.	Build ingestion pipelines for:
	•	Current RMS CSV
	•	SOP documents
	•	Historic events
	3.	Prove ROI through internal pilot shows.
	4.	Prepare the system for Current RMS API integration in v2/v3.

⸻

5. Full Project Scope (Untrimmed)

5.1 In-Scope v1

A. Event Specification Intake
	•	Web UI form for event data
	•	Structured JSON payload
	•	Input includes:
	•	Event info
	•	Rooms
	•	Technical requirements (audio/video/lighting/staging/power)
	•	Schedules
	•	Seating layouts
	•	Streaming flags
	•	Optional client names, budgets

B. AI-Generated Equipment Plans
	•	Per-room equipment list
	•	Each line includes:
	•	item_code
	•	item_name
	•	qty
	•	notes
	•	mapped product_group
	•	weight (if available)
	•	replacement_cost

C. AI-Generated Crew Plans
	•	Roles: A1, A2, V1, L1, L2, Stagehands, Riggers, Camera Ops
	•	Times: Load-in, show call, load-out
	•	Notes and assumptions

D. AI-Generated Trucking Estimates
	•	Truck count
	•	Load assumptions
	•	Weight totals
	•	Room-by-room distribution
	•	Flight-pack friendliness notes (if needed)

E. Knowledge Base / RAG
	•	Indexing the following in a vector DB:
	•	Current RMS products
	•	Current RMS stock levels
	•	SOPs
	•	Historic event plans
	•	Reference shows
	•	Retrieval logic based on:
	•	Event type
	•	Room type
	•	Inventories needed
	•	Technical requirements

F. Backend Architecture
	•	FastAPI backend
	•	Hugging Face Inference API client
	•	Vector DB wrapper
	•	Data validation
	•	Prompt construction & formatting
	•	JSON schema validation
	•	CSV exporters
	•	DB persistence

G. Front-End Architecture
	•	Browser-based UI
	•	Event editor
	•	Room builder
	•	Requirements editor
	•	Plan output viewer
	•	CSV download buttons
	•	Login page
	•	Dashboard

H. Output Formats
	•	Full EventPlan JSON
	•	equipment.csv
	•	crew.csv
	•	summary.txt

⸻

5.2 Out-of-Scope v1
	•	Real-time show control
	•	Live signal-flow design
	•	Automatic booking in Current RMS
	•	Inventory availability checks
	•	Financial quoting engine with taxes & discounts
	•	Multi-user collaboration features
	•	Mobile app
	•	Multi-organization tenants

⸻

6. Stakeholders

Primary Users
	•	Technical PMs
	•	Production Managers
	•	TDs
	•	Warehouse Managers
	•	Estimators

Stakeholders
	•	Legion AVS
	•	INT
	•	Lunaverse
	•	External AV firms (future)

⸻

7. User Stories

US-01: Generate Pull List

“As a TPM I want to enter show details and get an equipment pull list mapped to real Current RMS inventory.”

US-02: Generate Crew Plan

“As a PM I want crew role suggestions and hours.”

US-03: Estimate Trucking

“As a logistics manager I want a truck count and load assumptions.”

US-04: Reference Historic Shows

“As a PM I want past similar shows factored into recommendations.”

US-05: Export to CSV

“As a PM I want ready-to-import equipment and crew CSVs.”

US-06: Iteration

“As a PM I want to adjust event details and regenerate plans quickly.”

⸻

8. Functional Requirements

FR-01: Event Intake Validation

The backend must validate the EventSpec JSON against the full schema (provided later in this document).

FR-02: RAG Retrieval

Must retrieve:
	•	X most relevant inventory items
	•	SOPs
	•	Similar historic events
	•	Standard kits
	•	Product metadata (weight, power, replacement cost)

FR-03: AI Engine

Must produce structured JSON matching the EventPlan schema exactly.

FR-04: Equipment Mapping

Every equipment line must map to a real Current RMS product via either:
	•	current_product_id, or
	•	fallback nearest-match logic (flagged in notes)

FR-05: CSV Export

Must generate valid equipment.csv and crew.csv.

FR-06: Database Storage

Must store → events, event specs, event plans, equipment lines, crew lines.

FR-07: Authentication

JWT login required for the front end.

⸻

9. Non-Functional Requirements

NFR-01: Performance

20 seconds or less per /plan-event.

NFR-02: Reliability

Dockerized services, restart-safe.

NFR-03: Security
	•	Tokens required
	•	No external data storage
	•	No cloud logs
	•	Prompt text must be hashed, not saved

NFR-04: Maintainability

Everything stored with readable docs & comments.

⸻

10. Technical Architecture (Complete)

Backend:
	•	Python 3.11
	•	FastAPI
	•	SQLAlchemy
	•	Pydantic (schemas)
	•	Uvicorn

LLM Engine:
	•	Hugging Face Inference Endpoints
	•	Llama 3 (8B–13B)
	•	Quantized weights (int4/int8)

Vector Database:
	•	Chroma or Qdrant
	•	Embeddings: Instructor, E5-large, or HF embeddings

Database:
	•	Postgres
(Or SQLite for local dev)

Reverse Proxy:
	•	Caddy (preferred)
	•	Nginx (optional)

Front-End:
	•	Vue, React, or Svelte
	•	Vite bundler

⸻

11. Services & Components

Services
	•	Auth
	•	EventSpec storage
	•	EventPlan generation
	•	Embedding & RAG
	•	CSV export
	•	Historic ingestion
	•	Inventory ingestion

Workers
	•	Embedding worker
	•	Reindex worker

Background Tasks
	•	Rebuild embeddings
	•	Data cleanup
	•	Logging

⸻

12. Deployment
	•	Docker Compose with:
	•	api
	•	vector-db
	•	postgres
	•	front-end
	•	caddy
	•	Environment variables stored in .env

⸻

END OF PART 1

Part 2 continues with:

✔ Full EventSpec JSON Schema (complete, untrimmed)
✔ Full EventPlan JSON Schema (complete, untrimmed)
✔ Database Schema (all tables, untrimmed)
✔ Entity Relationship Model (all relations)
✔ API Routes (full definitions)
✔ Prompt Files (full system, format, user instructions)
✔ RAG Strategy
✔ Front-End UX Specification (detailed)
✔ Developer Bootstrapping Instructions


Here is PART 2 — the complete untrimmed technical core of the system.

This includes:

✔ Full EventSpec JSON Schema (complete)
✔ Full EventPlan JSON Schema (complete)
✔ Database Tables & Relations (full SQL schema)
✔ Entity Relationship Model (written-out ERD)
✔ Inventory ingestion formats (Current RMS–aligned)
✔ Historic event ingestion formats
✔ RAG retrieval definition

Part 3 will continue with:
	•	Full API Specifications
	•	Full Prompt Files
	•	Full Front-End UX Specification
	•	Full Repo Structure
	•	Developer Bootstrapping Instructions

⸻

PART 2 — SCHEMAS, DATA MODELS, TABLES, RELATIONS, RAG LAYER

⸻

SECTION A — FULL EVENT SPEC JSON SCHEMA (UNTRIMMED)

This is the exact complete schema the backend will validate against.

Store this as:
/docs/schemas/event_spec.json

{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "EventSpec",
  "type": "object",
  "required": [
    "event_name",
    "client_name",
    "start_date",
    "end_date",
    "venue",
    "city",
    "state",
    "country",
    "timezone",
    "rooms"
  ],
  "properties": {
    "event_name": { "type": "string" },
    "client_name": { "type": "string" },
    "start_date": { "type": "string", "format": "date" },
    "end_date": { "type": "string", "format": "date" },
    "venue": { "type": "string" },
    "city": { "type": "string" },
    "state": { "type": "string" },
    "country": { "type": "string" },
    "timezone": { "type": "string" },
    "expected_attendance": { "type": "integer" },

    "schedule_notes": { "type": "string" },

    "rooms": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "name",
          "type",
          "capacity",
          "days_active",
          "audio",
          "video",
          "lighting",
          "staging",
          "power",
          "schedule"
        ],
        "properties": {
          "name": { "type": "string" },
          "type": { "type": "string", "enum": ["GS", "Breakout", "Panel", "Workshop", "Expo", "Other"] },
          "capacity": { "type": "integer" },

          "days_active": {
            "type": "array",
            "items": { "type": "string", "format": "date" }
          },

          "layout": {
            "type": "string",
            "enum": ["Theater", "Classroom", "Rounds", "U-Shape", "Square", "Custom"]
          },

          "audio": {
            "type": "object",
            "properties": {
              "inputs_needed": { "type": "integer" },
              "mics": {
                "type": "array",
                "items": {
                  "type": "string",
                  "enum": ["Lavalier", "Handheld", "Podium", "DPA", "Countryman", "Headset", "Wireless", "Wired", "Comms"]
                }
              },
              "playback": { "type": "boolean" },
              "pa_coverage": { "type": "string" }
            }
          },

          "video": {
            "type": "object",
            "properties": {
              "screens": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "size_in": { "type": "integer" },
                    "count": { "type": "integer" },
                    "placement": { "type": "string" }
                  }
                }
              },
              "projectors": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "lumens": { "type": "integer" },
                    "count": { "type": "integer" },
                    "lens": { "type": "string" }
                  }
                }
              },
              "primary_display_type": {
                "type": "string",
                "enum": ["LED Wall", "Projector", "TV/Monitor", "None"]
              },
              "led_wall": {
                "type": "object",
                "properties": {
                  "width_ft": { "type": "number" },
                  "height_ft": { "type": "number" },
                  "pitch_mm": { "type": "number" }
                }
              },
              "recording": { "type": "boolean" },
              "livestream": { "type": "boolean" },
              "cameras": {
                "type": "number"
              }
            }
          },

          "lighting": {
            "type": "object",
            "properties": {
              "basic_wash": { "type": "boolean" },
              "uplights": { "type": "integer" },
              "moving_heads": { "type": "integer" },
              "console_required": { "type": "boolean" }
            }
          },

          "staging": {
            "type": "object",
            "properties": {
              "stage_width_ft": { "type": "number" },
              "stage_depth_ft": { "type": "number" },
              "stage_height_ft": { "type": "number" },
              "skirting": { "type": "boolean" },
              "pipe_and_drape": {
                "type": "object",
                "properties": {
                  "height_ft": { "type": "number" },
                  "linear_ft": { "type": "number" }
                }
              }
            }
          },

          "power": {
            "type": "object",
            "properties": {
              "dedicated_circuits": { "type": "integer" },
              "venue_power_notes": { "type": "string" }
            }
          },

          "schedule": {
            "type": "object",
            "properties": {
              "load_in": { "type": "string" },
              "rehearsal": { "type": "string" },
              "show_start": { "type": "string" },
              "show_end": { "type": "string" },
              "load_out": { "type": "string" }
            }
          },

          "additional_notes": { "type": "string" }
        }
      }
    },

    "general_notes": { "type": "string" }
  }
}


⸻

SECTION B — FULL EVENT PLAN JSON SCHEMA (UNTRIMMED)

Store as:
/docs/schemas/event_plan.json

This is exactly what the AI must return.

{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "EventPlan",
  "type": "object",
  "required": [
    "event_id",
    "event_name",
    "summary",
    "assumptions",
    "rooms",
    "trucking",
    "metadata"
  ],
  "properties": {
    "event_id": { "type": "string" },
    "event_name": { "type": "string" },

    "summary": { "type": "string" },

    "assumptions": {
      "type": "array",
      "items": { "type": "string" }
    },

    "rooms": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["room_id", "name", "equipment", "crew"],
        "properties": {
          "room_id": { "type": "string" },
          "name": { "type": "string" },

          "equipment": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["item_code", "name", "qty"],
              "properties": {
                "current_product_id": { "type": "string" },
                "item_code": { "type": "string" },
                "name": { "type": "string" },
                "product_group_name": { "type": "string" },
                "qty": { "type": "number" },
                "unit_type": { "type": "string" },
                "weight_total": { "type": "number" },
                "replacement_charge": { "type": "number" },
                "notes": { "type": "string" },
                "source": { "type": "string", "enum": ["ai", "fallback", "manual"] }
              }
            }
          },

          "crew": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["role", "qty"],
              "properties": {
                "role": { "type": "string" },
                "qty": { "type": "integer" },
                "hours_in": { "type": "number" },
                "hours_show": { "type": "number" },
                "hours_out": { "type": "number" },
                "bill_rate": { "type": "number" },
                "notes": { "type": "string" }
              }
            }
          }
        }
      }
    },

    "trucking": {
      "type": "object",
      "required": ["estimated_trucks"],
      "properties": {
        "estimated_trucks": { "type": "integer" },
        "weight_total_lbs": { "type": "number" },
        "weight_by_room": {
          "type": "object",
          "additionalProperties": { "type": "number" }
        },
        "notes": { "type": "string" }
      }
    },

    "metadata": {
      "type": "object",
      "properties": {
        "model_used": { "type": "string" },
        "generation_time_sec": { "type": "number" },
        "retrieval_context_count": { "type": "integer" }
      }
    }
  }
}


⸻

SECTION C — FULL DATABASE SCHEMA (SQL + RELATIONS)

This is the complete relational model.
Store as:
/docs/database/schema.sql

⸻

TABLE: users

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL CHECK (role IN ('admin','pm','viewer')),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);


⸻

TABLE: events

CREATE TABLE events (
  id UUID PRIMARY KEY,
  user_id INTEGER REFERENCES users(id),

  event_name TEXT NOT NULL,
  client_name TEXT,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,

  venue TEXT NOT NULL,
  city TEXT NOT NULL,
  state TEXT NOT NULL,
  country TEXT NOT NULL,
  timezone TEXT NOT NULL,
  expected_attendance INTEGER,

  current_opportunity_id TEXT,
  current_organization_id TEXT,
  current_contact_id TEXT,
  current_venue_id TEXT,
  opportunity_status TEXT,

  custom_fields JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);


⸻

TABLE: rooms

CREATE TABLE rooms (
  id UUID PRIMARY KEY,
  event_id UUID REFERENCES events(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  type TEXT,
  capacity INTEGER,
  days_active JSONB,
  layout TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);


⸻

TABLE: room_requirements

CREATE TABLE room_requirements (
  id UUID PRIMARY KEY,
  room_id UUID REFERENCES rooms(id) ON DELETE CASCADE,
  audio JSONB,
  video JSONB,
  lighting JSONB,
  staging JSONB,
  power JSONB,
  schedule JSONB,
  other_notes TEXT
);


⸻

TABLE: current_products

CREATE TABLE current_products (
  id UUID PRIMARY KEY,
  current_product_id TEXT,
  name TEXT,
  description TEXT,
  product_group_name TEXT,
  product_group_desc TEXT,
  is_bulk_stock BOOLEAN,
  is_serialised_stock BOOLEAN,
  is_non_stock BOOLEAN,
  rental_price NUMERIC,
  rental_charge_period_name TEXT,
  rental_rate_definition_name TEXT,
  rental_revenue_group TEXT,
  sale_price NUMERIC,
  sale_revenue_group TEXT,
  replacement_charge NUMERIC,
  weight NUMERIC,
  power NUMERIC,
  barcode TEXT,
  icon_url TEXT,
  raw_json JSONB,
  embedding VECTOR(1024),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);


⸻

TABLE: current_stock_levels

CREATE TABLE current_stock_levels (
  id UUID PRIMARY KEY,
  current_product_id UUID REFERENCES current_products(id) ON DELETE CASCADE,
  current_stock_level_id TEXT,
  is_serialised BOOLEAN,
  asset_number TEXT,
  store_name TEXT,
  quantity INTEGER,
  status TEXT,
  custom_fields JSONB,
  raw_json JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);


⸻

TABLE: event_plans

CREATE TABLE event_plans (
  id UUID PRIMARY KEY,
  event_id UUID REFERENCES events(id) ON DELETE CASCADE,
  summary TEXT,
  assumptions JSONB,
  trucking JSONB,
  metadata JSONB,
  weight_total_lbs NUMERIC,
  weight_by_room JSONB,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);


⸻

TABLE: equipment_lines

CREATE TABLE equipment_lines (
  id UUID PRIMARY KEY,
  event_plan_id UUID REFERENCES event_plans(id) ON DELETE CASCADE,
  room_id UUID REFERENCES rooms(id) ON DELETE CASCADE,

  opportunity_group_name TEXT,
  opportunity_group_order INTEGER,

  current_product_id UUID REFERENCES current_products(id),
  current_stock_level_id UUID REFERENCES current_stock_levels(id),

  item_code TEXT,
  name TEXT,
  product_group_name TEXT,
  category TEXT,
  qty NUMERIC,
  unit_type TEXT,
  rental_price NUMERIC,
  replacement_charge NUMERIC,
  weight_total NUMERIC,

  is_accessory BOOLEAN,
  parent_equipment_line_id UUID,

  notes TEXT,
  source TEXT
);


⸻

TABLE: crew_lines

CREATE TABLE crew_lines (
  id UUID PRIMARY KEY,
  event_plan_id UUID REFERENCES event_plans(id) ON DELETE CASCADE,
  room_id UUID REFERENCES rooms(id) ON DELETE CASCADE,
  role TEXT,
  qty INTEGER,
  hours_in NUMERIC,
  hours_show NUMERIC,
  hours_out NUMERIC,
  bill_rate NUMERIC,
  total_bill NUMERIC,
  notes TEXT
);


⸻

TABLE: historic_events

CREATE TABLE historic_events (
  id UUID PRIMARY KEY,
  title TEXT,
  body TEXT,
  embedding VECTOR(1024),
  created_at TIMESTAMP DEFAULT NOW()
);


⸻

TABLE: template_documents

CREATE TABLE template_documents (
  id UUID PRIMARY KEY,
  title TEXT,
  body TEXT,
  doc_type TEXT,
  embedding VECTOR(1024),
  created_at TIMESTAMP DEFAULT NOW()
);


⸻

SECTION D — ENTITY RELATIONSHIP MODEL (FULL WRITTEN ERD)

users 1---* events

events 1---* rooms

rooms 1---1 room_requirements

events 1---* event_plans

event_plans 1---* equipment_lines
event_plans 1---* crew_lines

rooms 1---* equipment_lines
rooms 1---* crew_lines

current_products 1---* current_stock_levels

current_products 1---* equipment_lines
current_stock_levels 1---* equipment_lines

historic_events (standalone) available for RAG

template_documents (standalone) available for RAG

This ERD supports:
	•	multiple versions of event plans
	•	multiple rooms per event
	•	equipment and crew grouped per room
	•	mapping to real Current RMS products

⸻

SECTION E — INVENTORY INGESTION FORMAT (FULL)

The system expects a CSV exported from Current RMS with the following fields:

Name
Product ID
Product Group Name
Product Group Description
Is Bulk Stock
Is Serialized Stock
Is Non-Stock
Rental Price
Rental Charge Period Name
Rental Rate Definition Name
Rental Revenue Group
Sale Price
Sale Revenue Group
Replacement Charge
Barcode
Icon URL
Weight (custom field)
Power (custom field)
Description

All rows are embedded and stored.

⸻

SECTION F — STOCK LEVELS INGESTION FORMAT

Stock Level ID
Product ID
Is Serialized
Asset Number
Store Name
Quantity
Status
Custom Fields JSON


⸻

SECTION G — HISTORIC EVENT INGESTION FORMAT

Text or JSON:

{
  "title": "Vistage Chicago 2024",
  "body": "Full pull list, crew, and trucking for Vistage Chicago…"
}


⸻

SECTION H — SOP / TEMPLATE INGESTION FORMAT

{
  "title": "Standard GS Package",
  "doc_type": "sop",
  "body": "This GS requires… etc"
}


⸻

SECTION I — RAG RETRIEVAL STRATEGY (COMPLETE)

For each /plan-event request:
	1.	Convert event_spec to embedding
	2.	Retrieve:
	•	Top 40 inventory products
	•	Top 10 historic events
	•	Top 10 SOP documents
	3.	Deduplicate similar items
	4.	Prepare context block consisting of:
	•	inventory summaries
	•	prior show patterns
	•	standard package templates
	5.	Pass all into the full prompt builder
	6.	Format into:

SYSTEM
CONTEXT
FORMAT SPEC
USER EVENT



⸻

END OF PART 2

Part 3 will begin immediately with:

✔ Full API Specification (untrimmed)
✔ Full Prompt Files: system, context, format spec
✔ Full Front-End UX Specification
✔ Full Developer Bootstrapping Checklist
✔ Full Repo Structure

Below is PART 3 — a fully expanded, untrimmed, developer-ready continuation of the Master Document.

This part contains:

✔ Full API Specification (all routes, all bodies, all responses, all errors)
✔ Complete Prompt Files (System Prompt, Retrieval Context Template, JSON Format Spec, Validation Prompt)
✔ Full Front-End UX Specification (pages, flows, wireframes in text, data-binding info)
✔ Full Dev Bootstrapping Instructions
✔ Full Repo Structure (finalized)

Part 4 will contain:
	•	Full CSV Export Specifications
	•	Environment Variable Specification
	•	Error Handling Specification
	•	Logging & Telemetry Specification
	•	Deployment Instructions
	•	Configurable Settings Reference
	•	Future v2/v3 Extension Blueprint

Let’s continue.

⸻

PART 3 — API SPEC + PROMPTS + FRONT-END UX + DEV SETUP + REPO STRUCTURE

⸻

SECTION A — FULL API SPECIFICATION (UNTRIMMED)

Store as:
/docs/api-spec.md

This is a complete OpenAPI-like definition written for developers to build from.

⸻

🔹 1. AUTHENTICATION

POST /auth/login

Authenticate a user.

Request Body

{
  "email": "string",
  "password": "string"
}

Response

{
  "access_token": "jwt_token_string",
  "token_type": "bearer",
  "user": {
    "id": "uuid",
    "email": "string",
    "role": "admin|pm|viewer"
  }
}

Errors
	•	401: Invalid credentials
	•	403: Account disabled (future use)

⸻

🔹 2. EVENT MANAGEMENT

POST /events

Create a new event record.

Request Body: EventSpec (full schema)

Uses the EventSpec schema delivered in Part 2.

Response

{
  "event_id": "uuid",
  "status": "created"
}


⸻

GET /events/{event_id}

Return stored event (not plan).

Response

{
  "event": { ...full EventSpec... }
}


⸻

GET /events

List events (with pagination).

Query Params

page, limit, sort_by, search

Response

{
  "events": [ ... ],
  "pagination": { ... }
}


⸻

🔹 3. PLAN GENERATION

POST /plan-event

Primary endpoint. Generates an EventPlan.

Request Body

{
  "event_id": "uuid",
  "event_spec": { ...full EventSpec... }
}

Workflow
	1.	Validate schema
	2.	Save spec to DB
	3.	Run RAG
	4.	Construct prompt
	5.	Send to Hugging Face endpoint
	6.	Validate returned JSON (repair if needed)
	7.	Save EventPlan to DB
	8.	Return JSON

Response

Full EventPlan schema as defined in Part 2.

Errors
	•	400 invalid event spec
	•	422 LLM returned invalid JSON
	•	500 HF unreachable

⸻

GET /event-plans/{event_id}

Retrieve latest plan for an event.

Response

{
  "event_plan": { ...EventPlan... }
}


⸻

GET /event-plans/{event_id}/versions

List all versions.

⸻

🔹 4. INVENTORY INGESTION

POST /ingest/inventory

Upload CSV of Current RMS products.

Body

multipart/form-data with CSV file.

Response

{
  "products_ingested": 324,
  "embeddings_generated": 324
}


⸻

POST /ingest/stock-levels

Upload stock CSV.

⸻

POST /ingest/historic-events

Upload NDJSON or array of objects:

[{"title":"string","body":"string"}]


⸻

POST /ingest/templates

Upload SOP templates.

⸻

🔹 5. RAG OPERATIONS

POST /rebuild-embeddings

Re-embed everything.

⸻

🔹 6. EXPORTS

GET /export/equipment-csv/{event_id}

Returns downloadable CSV.

CSV columns
	•	room
	•	item_code
	•	item_name
	•	qty
	•	unit
	•	notes
	•	product_group
	•	rental_price
	•	replacement_charge
	•	total_weight

⸻

GET /export/crew-csv/{event_id}

Crew CSV:
	•	room
	•	role
	•	qty
	•	hours_in
	•	hours_show
	•	hours_out
	•	total_hours
	•	bill_rate

⸻

GET /export/summary/{event_id}

Plain-text plan summary.

⸻

🔹 7. META ENDPOINTS

GET /health

Returns basic system health.

⸻

END API SPEC

⸻

SECTION B — FULL PROMPT FILES (UNTRIMMED)

Store as:
	•	/docs/prompts/system_prompt.txt
	•	/docs/prompts/json_format_spec.txt
	•	/docs/prompts/context_template.txt
	•	/docs/prompts/validator_prompt.txt

⸻

🔹 system_prompt.txt

You are Lunaverse Show Brain, an elite Technical Director + Production Manager AI specializing in AV design, crew planning, and trucking logistics for corporate events.

Your responsibilities:
1. Interpret the EventSpec precisely.
2. Compare it with relevant inventory, templates, and prior events.
3. Produce equipment lists that directly map to the CURRENT_PRODUCTS collection.
4. Use fallback logic only if no item exists, and clearly note fallback usage.
5. Generate accurate crew plans aligned with industry practices.
6. Produce realistic trucking estimates with weight calculations.
7. Produce strictly VALID JSON that matches the EventPlan schema exactly.

Safety Requirements:
- Never hallucinate gear that doesn't exist in the real inventory unless fallback is unavoidable.
- Never omit required fields.
- Never break JSON validity.
- Always justify assumptions in `assumptions[]`.

Your tone:
- Professional and concise.
- No explanations outside the JSON.
- Avoid conversational phrasing.

Your output MUST be *only* the JSON object with no commentary.


⸻

🔹 json_format_spec.txt

THE OUTPUT MUST BE VALID JSON MATCHING EXACTLY THIS STRUCTURE:

{
  "event_id": "string",
  "event_name": "string",
  "summary": "string",
  "assumptions": ["string", ...],
  "rooms": [
    {
      "room_id": "string",
      "name": "string",
      "equipment": [
        {
          "current_product_id": "string or null",
          "item_code": "string",
          "name": "string",
          "product_group_name": "string",
          "qty": number,
          "unit_type": "string",
          "weight_total": number,
          "replacement_charge": number,
          "notes": "string",
          "source": "ai|fallback|manual"
        }
      ],
      "crew": [
        {
          "role": "string",
          "qty": integer,
          "hours_in": number,
          "hours_show": number,
          "hours_out": number,
          "bill_rate": number,
          "notes": "string"
        }
      ]
    }
  ],
  "trucking": {
    "estimated_trucks": integer,
    "weight_total_lbs": number,
    "weight_by_room": { "room_name": number, ... },
    "notes": "string"
  },
  "metadata": {
    "model_used": "string",
    "generation_time_sec": number,
    "retrieval_context_count": integer
  }
}

YOU MUST NOT ADD EXTRA FIELDS.
YOU MUST NOT REMOVE ANY REQUIRED FIELDS.


⸻

🔹 context_template.txt

CONTEXT FOR AI:

INVENTORY SUMMARY (TOP MATCHES):
{{inventory_docs}}

HISTORIC SHOWS (MOST RELEVANT):
{{historic_events}}

TEMPLATE DOCUMENTS (STANDARD KITS):
{{templates}}

INSTRUCTIONS:
- Use inventory_docs as your primary source of permitted equipment.
- Use historic_events to model typical quantities.
- Use templates to guide standard room packages.
- If EventSpec references LED walls, audio requirements, etc., map them to known product groups.
- Always match gear to the nearest correct Current RMS product if exact match is unavailable.


⸻

🔹 validator_prompt.txt

You will be given JSON. You must:

1. Validate JSON against the EventPlan schema.
2. If valid, return "VALID" + the original JSON exactly.
3. If INVALID:
   - Fix only structural issues (unquoted keys, trailing commas, etc.)
   - Do NOT change content meaningfully.
   - Return "REPAIRED" + the corrected JSON.

Your output must be JSON only.


⸻

SECTION C — FRONT-END UX SPEC (FULL)

Store as:
/docs/frontend-ux.md

This is a full developer hand-off for the web UI.

⸻

🔹 1. PAGE: Login
	•	Fields: email, password
	•	POST to /auth/login
	•	On success → store JWT in memory + localStorage
	•	On failure → “Invalid credentials”

⸻

🔹 2. PAGE: Dashboard
	•	Lists recent events
	•	Button: “New Event”
	•	Button: “View Event”

⸻

🔹 3. PAGE: Event Builder Wizard

Step 1: Event Details
	•	event_name
	•	client_name
	•	dates
	•	venue, city, state
	•	timezone
	•	expected_attendance

Step 2: Rooms Overview
	•	Add Room
	•	Edit Room
	•	Remove Room

Step 3: Room Editor
For each room:

Tabs Inside Room:

Audio:
	•	mics
	•	inputs_needed
	•	playback
	•	pa_coverage

Video:
	•	screens
	•	projectors
	•	LED wall dimensions
	•	recording
	•	livestream
	•	cameras

Lighting:
	•	wash
	•	uplighting
	•	moving heads
	•	console

Staging:
	•	stage dims
	•	drape
	•	skirting

Power:
	•	circuits
	•	venue power notes

Schedule:
	•	load in
	•	rehearsal
	•	show start/end
	•	load out

⸻

🔹 4. PAGE: Generate Plan
	•	Review event summary
	•	Button: “Generate Plan”
	•	Loading animation (15–30 sec)

When plan is returned:
	•	auto-save
	•	redirect → Plan Viewer

⸻

🔹 5. PAGE: Plan Viewer

Functional UI:

A. Summary Block
	•	Summary text
	•	Assumptions
	•	Trucking overview

B. Rooms List
For each room:
	•	Expandable accordion
	•	Equipment table
	•	Crew table
	•	Edit/Modify (future)

C. Export Buttons
	•	Download Equipment CSV
	•	Download Crew CSV
	•	Download Summary

D. Version History
	•	List previous plan versions
	•	Click to load version

⸻

SECTION D — DEVELOPER BOOTSTRAPPING INSTRUCTIONS

Store as:
/docs/dev-setup.md

This is the entire setup procedure.

⸻

1. Clone Repo

git clone <repo_url>
cd lunaverse-show-brain


⸻

2. Copy Env Template

cp .env.example .env

Fill in:
	•	HF API key
	•	DB credentials
	•	CORS origins
	•	JWT secret

⸻

3. Start Services

docker compose up -d

This launches:
	•	postgres
	•	vector-db
	•	backend api
	•	frontend
	•	caddy

⸻

4. Apply Database Migrations

Using Alembic or raw SQL:

alembic upgrade head

Or:

psql -f docs/database/schema.sql


⸻

5. Install Python deps (if running locally)

cd backend
pip install -r requirements.txt


⸻

6. Run Dev Server

uvicorn app.main:app --reload


⸻

7. Access Front-End

http://localhost/

⸻

8. Ingest Data
	1.	Upload Current RMS product CSV
	2.	Upload Stock Levels
	3.	Upload SOPs
	4.	Upload Historic Events
	5.	Run /rebuild-embeddings

⸻

9. Ready to Generate Plans

Send a POST to /plan-event with EventSpec JSON.

⸻

SECTION E — REPO STRUCTURE FINAL (UNTRIMMED)

Store as:
/docs/repo-structure.md

lunaverse-show-brain/
  backend/
    app/
      main.py
      config.py
      schemas/
        event_spec.py
        event_plan.py
      models/
        users.py
        events.py
        rooms.py
        room_requirements.py
        current_products.py
        current_stock_levels.py
        event_plans.py
        equipment_lines.py
        crew_lines.py
        historic_events.py
        template_documents.py
      routes/
        auth.py
        events.py
        plan_event.py
        ingest_inventory.py
        ingest_templates.py
        ingest_historic.py
        export_csv.py
        admin_tools.py
      services/
        llm_client.py
        rag.py
        planner_engine.py
        csv_exporter.py
        embeddings.py
        validation.py
      db/
        session.py
        base.py
      auth/
        jwt_auth.py
        password_hash.py
    Dockerfile
    requirements.txt

  frontend/
    src/
      pages/
        Login.vue
        Dashboard.vue
        EventWizard.vue
        RoomEditor.vue
        GeneratePlan.vue
        PlanViewer.vue
      components/
        RoomCard.vue
        EquipmentTable.vue
        CrewTable.vue
        TruckingSummary.vue
        VersionHistory.vue
      api/
        client.js
        auth.js
        events.js
        plan.js
    package.json
    vite.config.js
    Dockerfile

  infrastructure/
    docker-compose.yml
    caddy/
      Caddyfile

  docs/
    scope-master.md
    api-spec.md
    dev-setup.md
    prompts/
      system_prompt.txt
      context_template.txt
      json_format_spec.txt
      validator_prompt.txt
    schemas/
      event_spec.json
      event_plan.json
    database/
      schema.sql
      migrations/

  .env.example
  README.md


⸻

END OF PART 3

Part 4 will include:

✔ CSV Export Specifications
✔ Logging & Telemetry Specifications
✔ Error Handling Rules
✔ Environment Variable Reference
✔ Deployment Guide
✔ Future v2/v3 Expansion Blueprint
✔ Full “What a developer builds first” guide


Alright, final boss round.
Here’s PART 4 — tying everything together so a developer could actually ship this thing.

This part includes:
	•	Full CSV export specifications
	•	Error handling model (status codes, error payloads, JSON repair rules)
	•	Logging & telemetry specification
	•	Environment variable reference (all keys, all meanings)
	•	Deployment guide (dev, staging, prod on your Lunaverse server)
	•	Configurable settings reference
	•	v2/v3 roadmap aligned with Current RMS
	•	“First 10 tasks” for a dev starting from zero

After this, your combined docs are effectively complete.

⸻

PART 4 — EXPORTS + ERRORS + LOGGING + ENV + DEPLOYMENT + ROADMAP

⸻

SECTION A — CSV EXPORT SPECIFICATIONS (FULL)

Store as:
/docs/csv-exports.md

These are the canonical CSV formats that /export/* must produce.

⸻

1. Equipment CSV Export

Endpoint:
GET /export/equipment-csv/{event_id}

Content-Type:
text/csv

File name pattern:
{event_name}_equipment_{YYYY-MM-DD}.csv

Columns (in order):
	1.	Room
	2.	Group
	3.	Item Code
	4.	Product Name
	5.	Product Group
	6.	Qty
	7.	Unit Type
	8.	Rental Price
	9.	Replacement Charge
	10.	Weight Total (lbs)
	11.	Current Product ID
	12.	Notes
	13.	Source

Example header row:

Room,Group,Item Code,Product Name,Product Group,Qty,Unit Type,Rental Price,Replacement Charge,Weight Total (lbs),Current Product ID,Notes,Source

Mapping from DB:
	•	Room → rooms.name (via equipment_lines.room_id)
	•	Group → equipment_lines.opportunity_group_name
	•	Item Code → equipment_lines.item_code
	•	Product Name → equipment_lines.name
	•	Product Group → equipment_lines.product_group_name
	•	Qty → equipment_lines.qty
	•	Unit Type → equipment_lines.unit_type
	•	Rental Price → equipment_lines.rental_price
	•	Replacement Charge → equipment_lines.replacement_charge
	•	Weight Total (lbs) → equipment_lines.weight_total
	•	Current Product ID → current_products.current_product_id (joined via equipment_lines.current_product_id)
	•	Notes → equipment_lines.notes
	•	Source → equipment_lines.source

⸻

2. Crew CSV Export

Endpoint:
GET /export/crew-csv/{event_id}

Content-Type:
text/csv

File name pattern:
{event_name}_crew_{YYYY-MM-DD}.csv

Columns (in order):
	1.	Room
	2.	Role
	3.	Qty
	4.	Hours In
	5.	Hours Show
	6.	Hours Out
	7.	Total Hours
	8.	Bill Rate
	9.	Total Bill
	10.	Notes

Example header row:

Room,Role,Qty,Hours In,Hours Show,Hours Out,Total Hours,Bill Rate,Total Bill,Notes

Mapping from DB:
	•	Room → rooms.name
	•	Role → crew_lines.role
	•	Qty → crew_lines.qty
	•	Hours In → crew_lines.hours_in
	•	Hours Show → crew_lines.hours_show
	•	Hours Out → crew_lines.hours_out
	•	Total Hours → hours_in + hours_show + hours_out
	•	Bill Rate → crew_lines.bill_rate
	•	Total Bill → crew_lines.total_bill
	•	Notes → crew_lines.notes

⸻

3. Summary TXT Export

Endpoint:
GET /export/summary/{event_id}

Content-Type:
text/plain

Structure:

Event: {event_name}
Client: {client_name}
Dates: {start_date} – {end_date}
Venue: {venue}, {city}, {state}, {country}

SUMMARY
-------
{summary}

ASSUMPTIONS
-----------
- {assumption 1}
- {assumption 2}
...

TRUCKING
--------
Estimated Trucks: {estimated_trucks}
Total Weight (lbs): {weight_total_lbs}

Weight by Room:
- {room_name}: {weight} lbs

ROOMS
-----
{for each room}
Room: {room_name}
Equipment Lines: {count}
Crew Lines: {count}

This file is just for quick email copy/paste.

⸻

SECTION B — ERROR HANDLING SPECIFICATION

Store as:
/docs/error-handling.md

⸻

1. Error Response Shape

All errors return JSON shaped like:

{
  "error": {
    "code": "string_machine_code",
    "message": "Human-readable explanation",
    "details": {
      "...": "optional extra"
    },
    "request_id": "uuid"
  }
}

HTTP Status → Codes
	•	400 → BAD_REQUEST
	•	401 → UNAUTHORIZED
	•	403 → FORBIDDEN
	•	404 → NOT_FOUND
	•	422 → UNPROCESSABLE_ENTITY
	•	500 → INTERNAL_SERVER_ERROR
	•	502 → UPSTREAM_LLM_ERROR

⸻

2. Validation Errors (EventSpec)
	•	Status: 400
	•	code: INVALID_EVENT_SPEC
	•	details includes list of field errors as returned by Pydantic / schema validator.

Example:

{
  "error": {
    "code": "INVALID_EVENT_SPEC",
    "message": "EventSpec failed validation",
    "details": {
      "missing_fields": ["event_name", "rooms[0].audio"],
      "schema_errors": [ ... ]
    },
    "request_id": "c6a3b8c2-..."
  }
}


⸻

3. LLM / JSON Errors

If HF endpoint fails:
	•	Status: 502
	•	code: UPSTREAM_LLM_ERROR

If HF returns invalid JSON twice:
	•	Status: 422
	•	code: INVALID_LLM_OUTPUT

⸻

4. JSON Repair Process

When /plan-event receives raw text from HF:
	1.	Try json.loads() directly.
	2.	If fail → run a “light repair”:
	•	Remove trailing commas
	•	Ensure keys are quoted
	•	Fix single quotes to double if consistent
	3.	Try json.loads() again.
	4.	If fail → optionally call validator_prompt to request corrected JSON.
	5.	If still invalid → return INVALID_LLM_OUTPUT.

At no point should the system silently change semantics (e.g., altering quantities). Repairs must be structural only.

⸻

SECTION C — LOGGING & TELEMETRY SPEC

Store as:
/docs/logging-telemetry.md

⸻

1. Logging Format

All logs are JSON lines (one JSON per line), with fields:

{
  "timestamp": "2025-11-22T21:07:34.123Z",
  "level": "INFO|WARN|ERROR",
  "service": "api|rag|llm|frontend",
  "event": "string_event_name",
  "request_id": "uuid",
  "user_id": "uuid or null",
  "route": "/plan-event",
  "extra": {
    "...": "context-dependent"
  }
}

Examples of event:
	•	EVENT_CREATED
	•	PLAN_GENERATION_STARTED
	•	PLAN_GENERATION_COMPLETED
	•	LLM_CALL_FAILED
	•	EMBEDDINGS_REBUILT

⸻

2. No Prompt/Spec Logging
	•	Never log full prompt text.
	•	Instead, log:
	•	prompt_hash (SHA-256)
	•	event_id
	•	model_used

Example:

{
  "timestamp": "...",
  "level": "INFO",
  "service": "llm",
  "event": "LLM_CALL_COMPLETED",
  "request_id": "uuid",
  "user_id": "uuid",
  "extra": {
    "event_id": "uuid",
    "model_used": "meta-llama3-8b-instruct",
    "prompt_hash": "a7f2c3e1..."
  }
}


⸻

3. Metrics / Telemetry

Optional, but recommended for future:
	•	Requests per endpoint
	•	LLM latency distribution
	•	Embedding latency
	•	Average plan size (number of lines per room)

Use Prometheus / Grafana or similar if you want later.

⸻

SECTION D — ENVIRONMENT VARIABLE SPEC

Store as:
/docs/env-reference.md

Here’s the canonical list. All of these must exist (with defaults where sensible).

⸻

Backend .env
	•	APP_ENV — development | staging | production
	•	APP_HOST — default 0.0.0.0
	•	APP_PORT — default 8000
	•	DATABASE_URL — e.g., postgresql+psycopg2://user:pass@db:5432/lunaverse
	•	VECTOR_DB_URL — connection string or host for Chroma/Qdrant
	•	VECTOR_DB_API_KEY — if needed
	•	HF_API_URL — full URL to your HF Inference Endpoint
	•	HF_API_KEY — secret token
	•	JWT_SECRET_KEY — long random string
	•	JWT_ALGORITHM — e.g., HS256
	•	JWT_ACCESS_TOKEN_EXPIRE_MINUTES — e.g., 1440
	•	CORS_ORIGINS — comma-separated list of allowed origins
	•	LOG_LEVEL — INFO | DEBUG | WARN | ERROR
	•	Optional Current RMS integration (v2+):
	•	CURRENT_RMS_SUBDOMAIN — yourcompany
	•	CURRENT_RMS_API_KEY or OAuth details

⸻

Frontend .env
	•	VITE_API_BASE_URL — e.g., https://showbrain.local/api

⸻

SECTION E — DEPLOYMENT GUIDE (LUNAVERSE SERVER)

Store as:
/docs/deployment.md

⸻

1. Prerequisites
	•	Ubuntu server with:
	•	Docker
	•	Docker Compose
	•	Domain or subdomain pointing to server (optional for prod)

⸻

2. Directory Layout on Server

Clone repo to:

/opt/lunaverse-show-brain

⸻

3. Configure .env Files
	•	/opt/lunaverse-show-brain/.env
	•	/opt/lunaverse-show-brain/backend/.env (if separate)
	•	/opt/lunaverse-show-brain/frontend/.env

⸻

4. Start Docker Stack

From project root:

docker compose pull
docker compose up -d


⸻

5. Run Migrations

docker compose exec api alembic upgrade head

or:

docker compose exec db psql -U postgres -d lunaverse -f /app/docs/database/schema.sql


⸻

6. Configure Caddy

infrastructure/caddy/Caddyfile example:

showbrain.local {
    reverse_proxy api:8000
}

showbrain-ui.local {
    reverse_proxy frontend:4173
}

Reload:

docker compose restart caddy


⸻

7. SSL (Production)

For real domains, Caddy can automatically obtain Let’s Encrypt certificates:

showbrain.yourdomain.com {
    reverse_proxy api:8000
}


⸻

8. Backups
	•	Nightly DB dumps via cron or a backup container
	•	Optionally snapshot vector DB as well

⸻

SECTION F — CONFIGURABLE SETTINGS REFERENCE

Store as:
/docs/configurable-settings.md

⸻

1. LLM Configuration
	•	model_name (HF endpoint)
	•	temperature (default 0.3)
	•	max_new_tokens (~2000)
	•	top_p, top_k if exposed

⸻

2. RAG Settings
	•	INVENTORY_TOP_K (e.g. 40)
	•	HISTORIC_TOP_K (e.g. 10)
	•	TEMPLATES_TOP_K (e.g. 10)
	•	Similarity search threshold

⸻

3. Crew Defaults / Rate Cards

Could be in config table or YAML:

crew_defaults:
  A1:
    hours_in: 4
    hours_show: 8
    hours_out: 4
    bill_rate: 75
  A2:
    ...

Backend must allow easy adjustments.

⸻

4. Trucking Heuristics

Config file like:

trucking:
  default_truck_volume_cuft: 3400
  panel_case_cuft: 20
  audio_case_cuft: 10
  lighting_case_cuft: 15

These are then used for quick cube approximations.

⸻

SECTION G — v2 / v3 ROADMAP BLUEPRINT

Store as:
/docs/roadmap.md

⸻

v2: Current RMS Integration & Availability
	•	Implement current_integration.py to:
	•	Push EventPlan → Current RMS Opportunity draft
	•	Create Opportunity Templates based on AI plans
	•	Add availability checks:
	•	For each current_product_id, check stock for event dates
	•	Mark lines as OK / Low / Short

v3: Multi-Tenant + Advanced Optimization
	•	Multi-company support (separate DB schemas or tenant_id fields)
	•	Case-level packing & 3D truck load planning
	•	Financial quoting with discounts and revenue projections
	•	Rich analytics for “what gear is used most / underutilized”

⸻

SECTION H — FIRST 10 TASKS FOR A DEVELOPER

Store as:
/docs/dev-onboarding-checklist.md
	1.	Set up environment & Docker
	•	Clone repo, configure .env, run compose.
	2.	Implement DB models (SQLAlchemy) for core tables
	•	users, events, rooms, room_requirements, event_plans, equipment_lines, crew_lines.
	3.	Implement EventSpec & EventPlan Pydantic schemas
	•	based on JSON schemas from docs.
	4.	Implement /auth/login with JWT
	•	password hashing + token issuing.
	5.	Implement basic /events CRUD
	•	Create event, fetch, list.
	6.	Implement inventory ingestion pipeline
	•	/ingest/inventory → parse CSV → current_products → embed.
	7.	Implement RAG service
	•	rag.py with functions: get_inventory_context, get_historic_context, get_template_context.
	8.	Implement llm_client
	•	wraps calls to HF endpoint using prompt templates.
	9.	Implement /plan-event
	•	Validate, store, retrieve context, build prompt, call LLM, repair JSON, store EventPlan & lines.
	10.	Implement front-end Event Builder + Plan Viewer
	•	Enough to go from login → event → plan → CSV.

Once those 10 are done, you basically have v1.

⸻

That’s it.
You now have:
	•	Full scope
	•	Full schemas
	•	Full data model
	•	Full API spec
	•	Full prompts
	•	Full UX flow
	•	Full deployment + env reference
	•	A clear dev starting path
