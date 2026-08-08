from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.stock_movement import MovementType

class StockMovementCreate(BaseModel):
    quantity: int
    reason: Optional[str] = None

class StockMovmentResponse(BaseModel):
    id: int
    quantity: int
    movement_type: MovementType
    reason: Optional[str]
    created_at: datetime
    product_id: int

    class Config:
        from_attributes = True