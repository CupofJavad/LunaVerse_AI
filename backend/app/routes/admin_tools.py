"""
Admin tools routes
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.current_products import CurrentProduct
from app.models.historic_events import HistoricEvent, TemplateDocument
from app.routes.auth import get_current_user
from app.models.users import User
from app.services.embeddings import generate_embedding

router = APIRouter()


@router.post("/rebuild-embeddings")
async def rebuild_embeddings(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Rebuild all embeddings"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Rebuild product embeddings
    products = db.query(CurrentProduct).all()
    product_count = 0
    for product in products:
        text = f"{product.name} {product.description or ''} {product.product_group_name or ''}"
        if text.strip():
            product.embedding = generate_embedding(text)
            product_count += 1
    
    # Rebuild historic event embeddings
    events = db.query(HistoricEvent).all()
    event_count = 0
    for event in events:
        text = f"{event.title} {event.body}"
        event.embedding = generate_embedding(text)
        event_count += 1
    
    # Rebuild template embeddings
    templates = db.query(TemplateDocument).all()
    template_count = 0
    for template in templates:
        text = f"{template.title} {template.body}"
        template.embedding = generate_embedding(text)
        template_count += 1
    
    db.commit()
    
    return {
        "products_rebuilt": product_count,
        "events_rebuilt": event_count,
        "templates_rebuilt": template_count
    }

