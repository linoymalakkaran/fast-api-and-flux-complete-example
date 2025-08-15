from fastapi import FastAPI
from app.core.middleware import log_requests
from app.routers import admin, user, auth as auth_router, address_book
from app.core import auth as core_auth

app = FastAPI(lifespan=core_auth.lifespan)

# Register logging middleware
app.middleware("http")(log_requests)

app.include_router(admin.router)
app.include_router(user.router)

app.include_router(auth_router.router)
app.include_router(address_book.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}
