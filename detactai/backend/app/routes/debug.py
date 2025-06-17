from fastapi import APIRouter
import os

router = APIRouter()

@router.get("/env")
def show_environment():
    return dict(os.environ)

@router.get("/model-info")
def model_information():
    return {
        "name": "YOLOv8n",
        "classes": 80,
        "input_size": "640x640"
    }
