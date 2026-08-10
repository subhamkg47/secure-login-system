from fastapi import FastAPI
from sqlalchemy import text

from database.database import Base, engine
from models.user import User
from models.file import File
from routers.auth import router as auth_router


app = FastAPI(
    title="Secure Login System API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {"message": "Secure Login System API is running!"}


@app.get("/test-db")
def test_database():
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"message": "Database connected successfully!"}
    except Exception as e:
        return {"error": str(e)}


app.include_router(auth_router)
