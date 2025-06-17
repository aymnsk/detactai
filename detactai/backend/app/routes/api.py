from fastapi import APIRouter, UploadFile, File
from app.core.detection import detect_objects
import os

router = APIRouter()

@router.post("/detect/image")
async def detect_image(file: UploadFile = File(...)):
    # Save uploaded file
    temp_path = f"app/temp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        buffer.write(await file.read())
    
    # Process detection
    results = detect_objects(temp_path)
    
    return {
        "filename": file.filename,
        "detections": results["detections"],
        "output_url": f"/temp/{os.path.basename(results['output_path'])}"
    }
