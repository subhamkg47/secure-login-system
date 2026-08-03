from fastapi import FastAPI

app = FastAPI(
    title="Secure Login System API",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to Secure Login System API"
    }