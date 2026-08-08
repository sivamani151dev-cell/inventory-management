from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product
from app.models.stock_movement import StockMovement, MovementType
from app.models.user import User
from app.schemas.stock_movement import StockMovementCreate, StockMovementResponse
from app.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/stock", tags=["Stock"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/in/{product_id}", response_model=StockMovementResponse, status_code=201)
def stock_in(product_id: int, movement: StockMovementCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id, Product.owner_id == current_user.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product.stock_quantity += movement.quantity
    new_movement = StockMovement(
        quantity=movement.quantity,
        movement_type=MovementType.stock_in,
        reason=movement.reason,
        product_id=product_id
    )
    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)
    logger.info(f"Stock in: {movement.quantity} units added to product {product_id}")
    return new_movement

@router.post("/out/{product_id}", response_model=StockMovementResponse, status_code=201)
def stock_out(product_id: int, movement: StockMovementCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id, Product.owner_id == current_user.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock_quantity < movement.quantity:
        raise HTTPException(status_code=400, detail=f"Insufficient stock. Available: {product.stock_quantity}")
    product.stock_quantity -= movement.quantity
    new_movement = StockMovement(
        quantity=movement.quantity,
        movement_type=MovementType.stock_out,
        reason=movement.reason,
        product_id=product_id
    )
    db.add(new_movement)
    db.commit()
    db.refresh(new_movement)
    logger.info(f"Stock out: {movement.quantity} units removed from product {product_id}")
    return new_movement

@router.get("/history/{product_id}", response_model=list[StockMovementResponse])
def get_stock_history(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    product = db.query(Product).filter(Product.id == product_id, Product.owner_id == current_user.id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    movements = db.query(StockMovement).filter(StockMovement.product_id == product_id).all()
    return movements