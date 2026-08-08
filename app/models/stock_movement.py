from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class MovementType(enum.Enum):
    stock_in = "stock_in"
    stock_out = "stock_out"

class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, nullable=False)
    movement_type = Column(Enum(MovementType), nullable=False)
    reason = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    product_id = Column(Integer, ForeignKey("products.id"))