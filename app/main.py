
from fastapi import FastAPI, UploadFile, File, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.image import Image
from app.models.log import APILog
from app.schemas.image import ImageOut, ImageCreate
from app.schemas.log import APILogOut
from app.utils.image_utils import validate_image, save_image, generate_thumbnail
from PIL import Image as PILImage
from app.utils.tagging import get_image_tags
import os
from datetime import datetime

app = FastAPI(title="Image Upload, Processing & Search API")

UPLOAD_DIR = "uploads"
THUMBNAIL_DIR = "thumbnails"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(THUMBNAIL_DIR, exist_ok=True)

Base.metadata.create_all(bind=engine)

def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

from fastapi.security import APIKeyQuery
from fastapi import Security
api_key_query = APIKeyQuery(name="token", auto_error=True)

def verify_token(api_key: str = Security(api_key_query)) -> str:
	if api_key != "mysecrettoken":
		raise HTTPException(status_code=401, detail="Invalid token")
	return api_key

@app.post("/upload", response_model=ImageOut)
def upload_image(file: UploadFile = File(...), db: Session = Depends(get_db), api_key: str = Security(verify_token)):
	try:
		img = validate_image(file)
		filename = f"{datetime.utcnow().timestamp()}_{file.filename}"
		file_path = os.path.join(UPLOAD_DIR, filename)
		thumb_path = os.path.join(THUMBNAIL_DIR, filename)
		save_image(img, file_path)
		generate_thumbnail(img, thumb_path)
		# Reload image from disk for tagging to avoid file pointer issues
		img_for_tagging = PILImage.open(file_path)
		tags = get_image_tags(img_for_tagging)
		image_obj = Image(
			filename=filename,
			size=os.path.getsize(file_path),
			width=img.width,
			height=img.height,
			thumbnail_path=thumb_path,
			# Add tags field if you update the model
		)
		db.add(image_obj)
		db.commit()
		db.refresh(image_obj)
		log = APILog(action="upload", details=f"Uploaded {filename} with tags {tags}")
		db.add(log)
		db.commit()
		return image_obj
	except Exception as e:
		import traceback
		error_type = type(e).__name__
		error_msg = str(e)
		tb = traceback.format_exc()
		raise HTTPException(status_code=500, detail=f"{error_type}: {error_msg}\n{tb}")


@app.get("/images", response_model=list[ImageOut])
def list_images(page: int = 1, page_size: int = 10, db: Session = Depends(get_db)):
	skip = (page - 1) * page_size
	images = db.query(Image).offset(skip).limit(page_size).all()
	log = APILog(action="list", details=f"Listed images page {page} size {page_size}")
	db.add(log)
	db.commit()
	return images


@app.get("/search", response_model=list[ImageOut])
def search_images(
	filename: str = Query(None),
	start_date: datetime = Query(None),
	end_date: datetime = Query(None),
	page: int = 1,
	page_size: int = 10,
	db: Session = Depends(get_db),
	api_key: str = Security(verify_token)
):
	query = db.query(Image)
	if filename:
		query = query.filter(Image.filename.ilike(f"%{filename}%"))
	if start_date:
		query = query.filter(Image.upload_timestamp >= start_date)
	if end_date:
		query = query.filter(Image.upload_timestamp <= end_date)
	skip = (page - 1) * page_size
	results = query.offset(skip).limit(page_size).all()
	log = APILog(action="search", details=f"Searched images: {filename}, {start_date}, {end_date}, page {page} size {page_size}")
	db.add(log)
	db.commit()
	return results

@app.get("/logs", response_model=list[APILogOut])
def get_logs(db: Session = Depends(get_db)):
	logs = db.query(APILog).order_by(APILog.timestamp.desc()).all()
	return logs
