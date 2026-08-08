from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.auth import decode_access_token
from fastapi.security import OAuth2PasswordBearer
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/categories", tags=["Categories"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    username = decode_access_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

@router.post("/", response_model=CategoryResponse, status_code=201)
def create_category(category: CategoryCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    new_category = Category(
        name=category.name,
        description=category.description,
        owner_id=current_user.id
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get("/", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Category).filter(Category.owner_id == current_user.id).all()

@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(category_id: int, update: CategoryUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == category_id, Category.owner_id == current_user.id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    if update.name is not None:
        category.name = update.name
    if update.description is not None:
        category.description = update.description
    db.commit()
    db.refresh(category)
    return category

@router.delete("/{category_id}", status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    category = db.query(Category).filter(Category.id == category_id, Category.owner_id == current_user.id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    db.delete(category)
    db.commit()
    return None