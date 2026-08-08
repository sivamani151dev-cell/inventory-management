from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int = 0
    low_stock_threshold: int = 10
    category_id: Optional[int] = None

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    low_stock_threshold: Optional[int] = None
    category_id: Optional[int] = None

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock_quantity: int
    low_stock_threshold: int
    created_at: datetime
    category_id: Optional[int]
    owner_id: int

    class Config: 
        from_attributes = True

class LowStockAlert(BaseModel):
    id: int
    name: str
    stock_quantity: int
    low_stock_threshold: int
    price: float