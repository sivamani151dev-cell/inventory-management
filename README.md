# 📦 Inventory Management System

A backend API for managing products, categories and stock movements built with FastAPI and PostgreSQL.

---

## 🚀 What This Project Does

- Register and login securely
- Create and manage product categories
- Add products with stock levels and pricing
- Track stock in/out movements
- Get low stock alerts when products fall below threshold
- View complete stock movement history

---

## 🧠 What I Learned Building This

- Multi-table relationships (Category → Product → StockMovement)
- Stock tracking with quantity updates
- Low stock threshold alerts
- Movement history logging
- Three-layer data model design

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.14 | Programming language |
| FastAPI | Web framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Alembic | Migrations |
| PyJWT | Authentication |
| bcrypt | Password hashing |
| Docker | Containerization |
| Uvicorn | Server |

---

## ⚙️ How To Run

### Without Docker:
```bash
git clone https://github.com/sivamani151dev-cell/inventory-management.git
cd inventory-management
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m alembic upgrade head
uvicorn app.main:app --reload
```

### With Docker:
```bash
docker-compose up --build
```

---

## 📡 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Register | ❌ |
| POST | `/auth/login` | Login | ❌ |

### Categories
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/categories/` | Create category | ✅ |
| GET | `/categories/` | Get all categories | ✅ |
| PUT | `/categories/{id}` | Update category | ✅ |
| DELETE | `/categories/{id}` | Delete category | ✅ |

### Products
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/products/` | Add product | ✅ |
| GET | `/products/` | Get all products | ✅ |
| GET | `/products/low-stock` | Low stock alert | ✅ |
| GET | `/products/{id}` | Get product | ✅ |
| PUT | `/products/{id}` | Update product | ✅ |
| DELETE | `/products/{id}` | Delete product | ✅ |

### Stock
| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/stock/in/{id}` | Add stock | ✅ |
| POST | `/stock/out/{id}` | Remove stock | ✅ |
| GET | `/stock/history/{id}` | Stock history | ✅ |

---

## 🎯 Project Type
Skill-Building Project — built to understand stock tracking, low stock alerts and movement history.