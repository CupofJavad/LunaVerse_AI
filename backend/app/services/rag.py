"""
RAG (Retrieval Augmented Generation) service
"""
from typing import List, Dict, Any
from app.config import settings
from app.services.embeddings import generate_embedding
from sqlalchemy.orm import Session
from sqlalchemy import text
import json


def get_inventory_context(
    event_spec_text: str,
    db: Session,
    top_k: int = None
) -> List[Dict[str, Any]]:
    """Retrieve top K inventory items based on event spec"""
    if top_k is None:
        top_k = settings.INVENTORY_TOP_K
    
    # Generate embedding for event spec
    query_embedding = generate_embedding(event_spec_text)
    
    # Simple similarity search (using cosine similarity on JSON array)
    # In production, use pgvector or dedicated vector DB
    query = text("""
        SELECT 
            id, current_product_id, name, description, product_group_name,
            replacement_charge, weight, rental_price
        FROM current_products
        WHERE embedding IS NOT NULL
        ORDER BY created_at DESC
        LIMIT :top_k
    """)
    
    results = db.execute(query, {"top_k": top_k}).fetchall()
    
    return [
        {
            "current_product_id": r.current_product_id,
            "name": r.name,
            "description": r.description,
            "product_group_name": r.product_group_name,
            "replacement_charge": float(r.replacement_charge) if r.replacement_charge else None,
            "weight": float(r.weight) if r.weight else None,
            "rental_price": float(r.rental_price) if r.rental_price else None
        }
        for r in results
    ]


def get_historic_context(
    event_spec_text: str,
    db: Session,
    top_k: int = None
) -> List[Dict[str, Any]]:
    """Retrieve top K historic events"""
    if top_k is None:
        top_k = settings.HISTORIC_TOP_K
    
    query = text("""
        SELECT id, title, body
        FROM historic_events
        ORDER BY created_at DESC
        LIMIT :top_k
    """)
    
    results = db.execute(query, {"top_k": top_k}).fetchall()
    
    return [
        {
            "title": r.title,
            "body": r.body
        }
        for r in results
    ]


def get_template_context(
    event_spec_text: str,
    db: Session,
    top_k: int = None
) -> List[Dict[str, Any]]:
    """Retrieve top K template documents"""
    if top_k is None:
        top_k = settings.TEMPLATES_TOP_K
    
    query = text("""
        SELECT id, title, body, doc_type
        FROM template_documents
        ORDER BY created_at DESC
        LIMIT :top_k
    """)
    
    results = db.execute(query, {"top_k": top_k}).fetchall()
    
    return [
        {
            "title": r.title,
            "body": r.body,
            "doc_type": r.doc_type
        }
        for r in results
    ]


def build_rag_context(event_spec_text: str, db: Session) -> str:
    """Build full RAG context string for prompt"""
    inventory = get_inventory_context(event_spec_text, db)
    historic = get_historic_context(event_spec_text, db)
    templates = get_template_context(event_spec_text, db)
    
    context_parts = []
    
    # Inventory summary
    if inventory:
        context_parts.append("INVENTORY SUMMARY (TOP MATCHES):")
        for item in inventory[:20]:  # Limit to top 20 for prompt size
            context_parts.append(f"- {item['name']} ({item['product_group_name']}): {item.get('description', 'N/A')}")
    
    # Historic shows
    if historic:
        context_parts.append("\nHISTORIC SHOWS (MOST RELEVANT):")
        for event in historic:
            context_parts.append(f"- {event['title']}: {event['body'][:200]}...")
    
    # Templates
    if templates:
        context_parts.append("\nTEMPLATE DOCUMENTS (STANDARD KITS):")
        for template in templates:
            context_parts.append(f"- {template['title']} ({template['doc_type']}): {template['body'][:200]}...")
    
    return "\n".join(context_parts)

