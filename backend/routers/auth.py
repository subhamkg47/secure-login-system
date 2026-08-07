from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy import select

from dependencies.auth import get_current_user
from schemas.user import UserCreate
from fastapi.security import OAuth2PasswordRequestForm
from database.database import get_db
from models.user import User
from utils.security import hash_password, verify_password
from utils.jwt_handler import (
    create_access_token,
    verify_access_token
)
router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)


@router.post("/register")
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.execute(
        select(User).where(User.email == user.email)
    ).scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully!",
        "email": new_user.email
    }

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    existing_user = db.execute(
        select(User).where(User.email == form_data.username)
    ).scalar_one_or_none()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        form_data.password,
        existing_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
    data={"sub": existing_user.email}
)

    return {
    "access_token": access_token,
    "token_type": "bearer"
    }

@router.get("/profile")
def get_profile(
    current_user = Depends(get_current_user)
):
    return {
        "message": "Protected route accessed!",
        "user": current_user["sub"]
    }