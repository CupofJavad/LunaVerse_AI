"""
Lunaverse Show Brain v1 - FastAPI Main Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import auth, events, plan_event, ingest_inventory, ingest_templates, ingest_historic, export_csv, admin_tools

app = FastAPI(
    title="Lunaverse Show Brain API",
    description="Event production planning engine with AI-generated equipment, crew, and trucking plans",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(events.router, prefix="/events", tags=["Events"])
app.include_router(plan_event.router, prefix="/plan-event", tags=["Plan Generation"])
app.include_router(ingest_inventory.router, prefix="/ingest", tags=["Ingestion"])
app.include_router(ingest_templates.router, prefix="/ingest", tags=["Ingestion"])
app.include_router(ingest_historic.router, prefix="/ingest", tags=["Ingestion"])
app.include_router(export_csv.router, prefix="/export", tags=["Exports"])
app.include_router(admin_tools.router, prefix="/admin", tags=["Admin"])


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "lunaverse-show-brain"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)

