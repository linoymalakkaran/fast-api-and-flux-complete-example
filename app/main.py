from fastapi import FastAPI, Request
import json
from datetime import datetime
from app.db import SessionLocal
from app.models import Log
from app.routers import admin, user, auth as auth_router, address_book
from app.core import auth as core_auth


app = FastAPI(lifespan=core_auth.lifespan)

# Logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    body = await request.body()
    log_entry = Log(
        method=request.method,
        path=request.url.path,
        query_params=json.dumps(dict(request.query_params)),
        body=body.decode() if body else None,
        timestamp=datetime.utcnow().isoformat()
    )
    print(f"Request: {log_entry.method} {log_entry.path} Params: {log_entry.query_params} Body: {log_entry.body}")
    db = SessionLocal()
    try:
        db.add(log_entry)
        db.commit()
    finally:
        db.close()
    response = await call_next(request)
    return response

app.include_router(admin.router)
app.include_router(user.router)

app.include_router(auth_router.router)
app.include_router(address_book.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
