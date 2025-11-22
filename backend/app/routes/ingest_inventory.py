"""
Inventory ingestion routes
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.models.current_products import CurrentProduct, CurrentStockLevel
from app.routes.auth import get_current_user
from app.models.users import User
from app.services.embeddings import generate_embedding
import csv
import io
import uuid

router = APIRouter()


@router.post("/inventory")
async def ingest_inventory(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload CSV of Current RMS products"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    csv_content = io.StringIO(content.decode('utf-8'))
    reader = csv.DictReader(csv_content)
    
    products_ingested = 0
    embeddings_generated = 0
    
    for row in reader:
        # Map CSV columns to model fields
        product = CurrentProduct(
            id=uuid.uuid4(),
            current_product_id=row.get("Product ID"),
            name=row.get("Name"),
            description=row.get("Description"),
            product_group_name=row.get("Product Group Name"),
            product_group_desc=row.get("Product Group Description"),
            is_bulk_stock=row.get("Is Bulk Stock", "").lower() == "true",
            is_serialised_stock=row.get("Is Serialized Stock", "").lower() == "true",
            is_non_stock=row.get("Is Non-Stock", "").lower() == "true",
            rental_price=float(row.get("Rental Price", 0)) if row.get("Rental Price") else None,
            rental_charge_period_name=row.get("Rental Charge Period Name"),
            rental_rate_definition_name=row.get("Rental Rate Definition Name"),
            rental_revenue_group=row.get("Rental Revenue Group"),
            sale_price=float(row.get("Sale Price", 0)) if row.get("Sale Price") else None,
            sale_revenue_group=row.get("Sale Revenue Group"),
            replacement_charge=float(row.get("Replacement Charge", 0)) if row.get("Replacement Charge") else None,
            weight=float(row.get("Weight", 0)) if row.get("Weight") else None,
            power=float(row.get("Power", 0)) if row.get("Power") else None,
            barcode=row.get("Barcode"),
            icon_url=row.get("Icon URL"),
            raw_json=row
        )
        
        # Generate embedding from name + description
        text_for_embedding = f"{product.name} {product.description or ''} {product.product_group_name or ''}"
        if text_for_embedding.strip():
            product.embedding = generate_embedding(text_for_embedding)
            embeddings_generated += 1
        
        db.add(product)
        products_ingested += 1
    
    db.commit()
    
    return {
        "products_ingested": products_ingested,
        "embeddings_generated": embeddings_generated
    }


@router.post("/stock-levels")
async def ingest_stock_levels(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload stock levels CSV"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    csv_content = io.StringIO(content.decode('utf-8'))
    reader = csv.DictReader(csv_content)
    
    stock_levels_ingested = 0
    
    for row in reader:
        # Find product by current_product_id
        product_id = row.get("Product ID")
        product = db.query(CurrentProduct).filter(CurrentProduct.current_product_id == product_id).first()
        
        if not product:
            continue  # Skip if product not found
        
        stock_level = CurrentStockLevel(
            id=uuid.uuid4(),
            current_product_id=product.id,
            current_stock_level_id=row.get("Stock Level ID"),
            is_serialised=row.get("Is Serialized", "").lower() == "true",
            asset_number=row.get("Asset Number"),
            store_name=row.get("Store Name"),
            quantity=int(row.get("Quantity", 0)) if row.get("Quantity") else 0,
            status=row.get("Status"),
            raw_json=row
        )
        
        db.add(stock_level)
        stock_levels_ingested += 1
    
    db.commit()
    
    return {"stock_levels_ingested": stock_levels_ingested}

