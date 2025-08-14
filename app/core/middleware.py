from fastapi import Request
from app.db import SessionLocal
from app.models import Log
import json
from datetime import datetime

# Logging middleware (runs before and after every request)
async def log_requests(request: Request, call_next):
    print(f"[Middleware] Before request: {request.method} {request.url.path}")
    response = await call_next(request)
    print(f"[Middleware] After request: {request.method} {request.url.path}")
    # Optional: log to DB
    body = await request.body()
    log_entry = Log(
        method=request.method,
        path=request.url.path,
        query_params=json.dumps(dict(request.query_params)),
        body=body.decode() if body else None,
        timestamp=datetime.utcnow().isoformat()
    )
    db = SessionLocal()
    try:
        db.add(log_entry)
        db.commit()
    finally:
        db.close()
    return response
