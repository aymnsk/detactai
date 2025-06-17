from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import os
import uuid
from ultralytics import YOLO

# Initialize FastAPI
app = FastAPI(title="DetectAI API", version="1.0.0")

# CORS Configuration (Critical for Vercel)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Setup paths (Vercel-specific)
BASE_DIR = Path(__file__).parent
MODEL_PATH = BASE_DIR / "models/yolov8n.pt"
TEMP_DIR = BASE_DIR / "temp"

# Create directories if they don't exist
os.makedirs(TEMP_DIR, exist_ok=True)

# Load YOLO model (with error handling)
try:
    model = YOLO(MODEL_PATH)
    print("✅ YOLOv8 model loaded successfully")
except Exception as e:
    print(f"❌ Failed to load model: {str(e)}")
    model = None

# Health check endpoint (required for Vercel)
@app.get("/")
async def health_check():
    return {
        "status": "active",
        "model_loaded": bool(model),
        "endpoints": {
            "docs": "/docs",
            "detect": "/api/detect/image",
            "debug": "/api/debug/model-info"
        }
    }

# Detection endpoint
@app.post("/api/detect/image")
async def detect_image(file: UploadFile = File(...)):
    if not model:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Save uploaded file
        file_ext = Path(file.filename).suffix
        temp_path = TEMP_DIR / f"{uuid.uuid4()}{file_ext}"
        
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Process detection
        results = model(temp_path)
        
        # Generate output
        output_path = TEMP_DIR / f"output_{temp_path.name}"
        results[0].save(filename=output_path)
        
        # Format detections
        detections = []
        for box in results[0].boxes:
            detections.append({
                "class": model.names[int(box.cls)],
                "confidence": float(box.conf),
                "bbox": box.xyxy[0].tolist()
            })
        
        return {
            "filename": file.filename,
            "detections": detections,
            "output_url": f"/temp/{output_path.name}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Debug endpoint
@app.get("/api/debug/model-info")
async def model_info():
    return {
        "status": "loaded" if model else "unloaded",
        "model": "YOLOv8n",
        "input_size": "640x640",
        "classes": 80 if model else 0
    }

# Serve static files (for output images)
app.mount("/temp", StaticFiles(directory=TEMP_DIR), name="temp")

# Vercel requires this for Python runtime
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
