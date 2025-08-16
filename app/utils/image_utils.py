from PIL import Image
import os
from fastapi import UploadFile, HTTPException

ALLOWED_FORMATS = ["JPEG", "PNG"]
MAX_SIZE_MB = 5
MAX_RESOLUTION = (4096, 4096)
THUMBNAIL_SIZE = (256, 256)

# Validate image format, size, resolution
def validate_image(file: UploadFile):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid image format.")
    contents = file.file.read()
    if len(contents) > MAX_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Image size exceeds limit.")
    file.file.seek(0)
    img = Image.open(file.file)
    if img.format not in ALLOWED_FORMATS:
        raise HTTPException(status_code=400, detail="Unsupported image format.")
    if img.size[0] > MAX_RESOLUTION[0] or img.size[1] > MAX_RESOLUTION[1]:
        raise HTTPException(status_code=400, detail="Image resolution too high.")
    return img

def save_image(img: Image, path: str):
    img.save(path)

def generate_thumbnail(img: Image, thumb_path: str):
    thumb = img.copy()
    thumb.thumbnail(THUMBNAIL_SIZE)
    thumb.save(thumb_path)
