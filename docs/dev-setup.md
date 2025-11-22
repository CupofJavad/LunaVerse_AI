# Developer Setup Guide

## Prerequisites

- Docker and Docker Compose installed
- Git
- (Optional) Python 3.11+ for local development
- (Optional) Node.js 18+ for local frontend development

## Quick Start

1. **Clone the repository**
   ```bash
   git clone <repo_url>
   cd lunaverse-show-brain
   ```

2. **Copy environment template**
   ```bash
   cp .env.example .env
   ```

3. **Configure environment variables**
   Edit `.env` and fill in:
   - `HF_API_URL` - Your Hugging Face Inference Endpoint URL
   - `HF_API_KEY` - Your Hugging Face API key
   - `JWT_SECRET_KEY` - A long random string for JWT signing

4. **Start services**
   ```bash
   cd infrastructure
   docker compose up -d
   ```

   This launches:
   - PostgreSQL database
   - FastAPI backend
   - Vue.js frontend
   - Caddy reverse proxy

5. **Initialize database**
   ```bash
   docker compose exec db psql -U postgres -d lunaverse -f /docker-entrypoint-initdb.d/schema.sql
   ```

   Or if using Alembic:
   ```bash
   docker compose exec api alembic upgrade head
   ```

6. **Create initial user**
   ```bash
   docker compose exec api python -c "
   from app.db.base import SessionLocal
   from app.models.users import User
   from app.auth.password_hash import hash_password
   db = SessionLocal()
   user = User(email='admin@example.com', password_hash=hash_password('admin123'), role='admin')
   db.add(user)
   db.commit()
   "
   ```

7. **Access the application**
   - Frontend: http://localhost:4173
   - API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

## Local Development

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Ingesting Data

1. **Upload Current RMS inventory**
   - Export products CSV from Current RMS
   - POST to `/ingest/inventory` with CSV file

2. **Upload stock levels**
   - POST to `/ingest/stock-levels` with CSV file

3. **Upload historic events**
   - POST to `/ingest/historic-events` with JSON array

4. **Upload templates/SOPs**
   - POST to `/ingest/templates` with JSON array

5. **Rebuild embeddings** (if needed)
   - POST to `/admin/rebuild-embeddings` (admin only)

## Testing

1. Login with your admin credentials
2. Create a new event
3. Generate a plan
4. View and export the plan

## Troubleshooting

- **Database connection errors**: Ensure PostgreSQL is running and DATABASE_URL is correct
- **LLM errors**: Verify HF_API_URL and HF_API_KEY are set correctly
- **CORS errors**: Check CORS_ORIGINS in .env matches your frontend URL

