from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import api, debug
import os

app = FastAPI(title="DetectAI API")

# Create temp directory if not exists
os.makedirs("app/temp", exist_ok=True)

# Mount endpoints
app.include_router(api.router, prefix="/api")
app.include_router(debug.router, prefix="/debug")

# Serve static files (output images)
app.mount("/temp", StaticFiles(directory="app/temp"), name="temp")

@app.get("/")
def health_check():
    return {"status": "active"}
