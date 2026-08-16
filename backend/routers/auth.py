from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from services.token_blacklist import blacklist_token
from sqlalchemy.orm import Session
from sqlalchemy import select

from datetime import datetime, timedelta

from dependencies.auth import get_current_user
from schemas.user import UserCreate, UserLogin
from database.database import get_db
from models.user import User
from utils.security import hash_password, verify_password
from utils.jwt_handler import create_access_token
router = APIRouter(
    prefix="",
    tags=["Authentication"]
)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
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

    # User does not exist
    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Check if account is currently locked
    if (
        existing_user.locked_until
        and existing_user.locked_until > datetime.utcnow()
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Check password
    if not verify_password(
        user.password,
        existing_user.hashed_password
    ):
        existing_user.failed_attempts += 1

        # Lock account after 5 failed attempts
        if existing_user.failed_attempts >= 5:
            existing_user.locked_until = (
                datetime.utcnow() + timedelta(minutes=15)
            )

        db.commit()

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Successful login
    existing_user.failed_attempts = 0
    existing_user.locked_until = None

    db.commit()

    access_token = create_access_token(
        data={"sub": existing_user.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me")
def get_profile(
    current_user: User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "email": current_user.email,
        "profile": {
            "fullName": "",
            "displayName": current_user.email.split("@")[0],
            "bio": "",
            "createdAt": current_user.created_at.isoformat() if current_user.created_at else None,
            "role": "user"
        }
    }

@router.post("/logout")
def logout(
    token: str = Depends(oauth2_scheme)
):
    blacklist_token(token)

    return {
        "message": "Logged out successfully"
    }
