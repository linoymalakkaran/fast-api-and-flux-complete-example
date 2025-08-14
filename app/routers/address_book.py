from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.auth import get_current_active_user, get_admin_user, get_db
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.auth import get_current_active_user, get_admin_user, get_db
from app.models import User, Contact
from app.schemas import ContactCreate, ContactUpdate, ContactOut, UserOut
from app.core.utils import log_dependency, log_decorator

router = APIRouter()

# Example: Dependency and custom decorator logging on a single endpoint
@router.get("/contacts", response_model=List[ContactOut], tags=["user"])
@log_decorator
async def list_my_contacts(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    _: None = Depends(log_dependency)
):
    contacts = db.query(Contact).filter(Contact.user_id == current_user.id).all()
    return contacts
@router.get("/contacts/{contact_id}", response_model=ContactOut, tags=["user"])
async def get_my_contact(
    contact_id: int = Path(..., ge=1),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    contact = db.query(Contact).filter(Contact.id == contact_id, Contact.user_id == current_user.id).first()
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact
