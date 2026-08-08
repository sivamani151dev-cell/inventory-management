from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, LowStockAlert
from app.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/products", tags=["Products"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        stock_quantity=product.stock_quantity,
        low_stock_threshold=product.low_stock_threshold,
        category_id=product.category_id,
        owner_id=current_user.id
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    logger.info(f"Product created: {product.name}")
    return new_product

@router.get("/low-stock", response_model=list[LowStockAlert])
def get_low_stock(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    products = db.query(Product).filter(
        Product.owner_id == current_user.id,
        Product.stock_quantity <= Product.low_stock_threshold
    ).all()
    return products

@router.get("/", response_model=list[ProductResponse])
def get_products(
    category_id: Optional[int] = None,
    keyword: Optional[str] = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Product).filter(Product.owner_id == current_user.id)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if keyword:
        query = query.filter(Product.name.ilike(f"%{keyword}%"))
    offset = (page - 1) * limit
    return query.offset(offset).limit(limit).all()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id, Product.owner_id == current_user.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, update: ProductUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id, Product.owner_id == current_user.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if update.name is not None:
        product.name = update.name
    if update.description is not None:
        product.description = update.description
    if update.price is not None:
        product.price = update.price
    if update.low_stock_threshold is not None:
        product.low_stock_threshold = update.low_stock_threshold
    if update.category_id is not None:
        product.category_id = update.category_id
    db.commit()
    db.refresh(product)
    return product

@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id, Product.owner_id == current_user.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return None