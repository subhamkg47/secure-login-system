from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from sqlalchemy import select

from schemas.user import UserCreate, UserLogin
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
    user: UserLogin,
    db: Session = Depends(get_db)
):
    existing_user = db.execute(
        select(User).where(User.email == user.email)
    ).scalar_one_or_none()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
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
    authorization: str = Header(...)
):
    token = authorization.replace("Bearer ", "")

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    return {
        "message": "Protected route accessed!",
        "user": payload["sub"]
    }