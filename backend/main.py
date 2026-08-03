from fastapi import FastAPI
from sqlalchemy import text
from database.database import engine

app = FastAPI(
    title="Secure Login System API",
    version="1.0.0"
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