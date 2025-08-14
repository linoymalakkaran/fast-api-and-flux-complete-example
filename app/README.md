# FastAPI Project Structure

- `app/` contains all application code
  - `main.py`: FastAPI entry point
  - `db.py`: Database connection/session
  - `models.py`: ORM models
  - `schemas.py`: Pydantic schemas
  - `core/`: Core logic (auth, etc.)
  - `routers/`: API routers (admin, user, auth)
