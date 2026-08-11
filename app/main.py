from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth, categories, products, stock
from fastapi.responses import RedirectResponse
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Inventory Management System",
    description="A backend API for managing products, categories and stock movements",
    version="1.0.0"
)

app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(stock.router)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")