from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session
from sqlalchemy import select

from database.database import get_db
from models.user import User

from utils.jwt_handler import verify_access_token
from services.token_blacklist import is_blacklisted


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/login"
)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    if is_blacklisted(token):
        raise HTTPException(
            status_code=401,
            detail="Token has been blacklisted"
        )

    payload = verify_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

    email = payload.get("sub")

    if not email:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    existing_user = db.execute(
        select(User).where(User.email == email)
    ).scalar_one_or_none()

    if existing_user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return existing_user
