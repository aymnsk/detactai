from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.routes import api, debug
from typing import List

# Initialize FastAPI app with proper metadata
app = FastAPI(
    title="DetectAI API",
    description="API for DetectAI services",
    version="1.0.0",
    docs_url="/docs",  # Enabled Swagger UI
    redoc_url="/redoc",  # Enabled ReDoc
)

# Configure CORS middleware with more secure defaults
# In production, replace "*" with specific allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Consider restricting this in production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["Content-Disposition"]  # Useful for file downloads
)

# Create temp directory if not exists in a more robust way
try:
    os.makedirs("app/temp", exist_ok=True)
except OSError as e:
    print(f"Error creating temp directory: {e}")

# Mount endpoints with tags for better documentation
app.include_router(
    api.router,
    prefix="/api",
    tags=["API Endpoints"],
)

app.include_router(
    debug.router,
    prefix="/debug",
    tags=["Debug Utilities"],
)

# Serve static files with proper cache control
app.mount(
    "/temp",
    StaticFiles(directory="app/temp", html=True),
    name="temp"
)

@app.get("/", tags=["Health Check"])
def health_check() -> dict:
    """Health check endpoint to verify API is running."""
    return {
        "status": "active",
        "version": app.version,
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
