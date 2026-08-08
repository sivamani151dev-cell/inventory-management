from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token
from app.models.user import User
from app.auth import hash_password, verify_password, create_access_token
from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter(prefix="/auth", tags=["Authentication"])
@router.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_email = db.query(User).filter(User.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    existing_username = db.query(User).filter(User.username == user.username).first()
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    new_user = User(
        email = user.email,
        username = user.username,
        hashed_password = hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    access_token = create_access_token(data = {"sub":user.username}, expires_delta=timedelta(minutes = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))))
    return {"access_token": access_token, "token_type": "bearer"}