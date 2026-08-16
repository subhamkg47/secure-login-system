from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from database.database import Base, engine
from models.user import User
from models.file import File
from routers.auth import router as auth_router
from routers import files


app = FastAPI(
    title="Secure Login System API",
    version="1.0.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"],
)



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
app.include_router(files.router)
