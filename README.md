
# Image Upload, Processing & Search API

## Features
- Upload JPEG/PNG images
- Validate format, size, resolution
- Generate and store thumbnails
- Store metadata in PostgreSQL or SQLite
- List and search images
- Log API activity
- Image tagging using ResNet18 (PyTorch/torchvision)
- Token-based authentication for protected endpoints

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. (Optional) Set up PostgreSQL and update `DATABASE_URL` in `app/database.py`, or use SQLite for local development.
3. Run migrations to create tables (see SQLAlchemy docs).
4. Start the server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Authentication
All protected endpoints require a token for access. The default token is:

```
mysecrettoken
```

You must provide this token as a query parameter in your requests:

```
http://127.0.0.1:8000/upload?token=mysecrettoken
```

Or in curl:

```
curl -X 'POST' \
  'http://127.0.0.1:8000/upload?token=mysecrettoken' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_image.png;type=image/png'
```

If you use any other token, the request will be rejected with a 401 error.

## API Docs
Visit `/docs` for Swagger UI and interactive API documentation.