

from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.auth import get_current_active_user, get_admin_user, get_db
from app.models import User, Contact
from app.schemas import UserOut, ContactCreate, ContactOut, UserCreate, ContactUpdate
from app.core.utils import log_dependency, log_decorator

router = APIRouter()

# Admin: Create user with contacts in one request
from pydantic import BaseModel
class UserWithContactsCreate(BaseModel):
    username: str
    password: str
    role: str
    contacts: Optional[List[ContactCreate]] = []

@router.post("/users_with_contacts", response_model=UserOut, tags=["admin"])
async def create_user_with_contacts(
    payload: UserWithContactsCreate,
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    # Create user
    from app.core.auth import get_password_hash
    user = User(
        username=payload.username,
        hashed_password=get_password_hash(payload.password),
        role=payload.role
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    # Add contacts
    contacts_out = []
    for contact in payload.contacts:
        new_contact = Contact(user_id=user.id, **contact.model_dump())
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        contacts_out.append(new_contact)
    user.contacts = contacts_out
    return user

# Admin: List all users with pagination
@router.get("/users", response_model=List[UserOut], tags=["admin"])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    users = db.query(User).offset(skip).limit(limit).all()
    return users

# Admin: Get user details
@router.get("/users/{user_id}", response_model=UserOut, tags=["admin"])
async def get_user(
    user_id: int = Path(..., ge=1),
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Admin: Add contact for any user
@router.post("/users/{user_id}/contacts", response_model=ContactOut, tags=["admin"])
async def add_contact_for_user(
    contact: ContactCreate,
    user_id: int = Path(..., ge=1),
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_contact = Contact(user_id=user_id, **contact.model_dump())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

# Admin: Update contact
@router.put("/contacts/{contact_id}", response_model=ContactOut, tags=["admin"])
async def update_contact(
    contact: ContactUpdate,
    contact_id: int = Path(..., ge=1),
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.model_dump(exclude_unset=True).items():
        setattr(db_contact, key, value)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# Admin: Delete contact
@router.delete("/contacts/{contact_id}", status_code=204, tags=["admin"])
async def delete_contact(
    contact_id: int = Path(..., ge=1),
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(db_contact)
    db.commit()
    return

# User: List own contacts (with logging examples)
@router.get("/contacts", response_model=List[ContactOut], tags=["user"])
@log_decorator
async def list_my_contacts(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    _: None = Depends(log_dependency)
):
    contacts = db.query(Contact).filter(Contact.user_id == current_user.id).all()
    return contacts

# User: View own contact
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
