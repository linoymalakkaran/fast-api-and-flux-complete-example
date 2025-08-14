from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.auth import get_current_active_user, get_admin_user, get_db
from app.models import User, Contact
from app.schemas import ContactCreate, ContactUpdate, ContactOut, UserOut

router = APIRouter()

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
    user_id: int = Path(..., ge=1),
    contact: ContactCreate = Depends(),
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_contact = Contact(user_id=user_id, **contact.dict())
    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)
    return new_contact

# Admin: Update contact
@router.put("/contacts/{contact_id}", response_model=ContactOut, tags=["admin"])
async def update_contact(
    contact_id: int = Path(..., ge=1),
    contact: ContactUpdate = Depends(),
    current_user: User = Depends(get_admin_user),
    db: Session = Depends(get_db)
):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if not db_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    for key, value in contact.dict(exclude_unset=True).items():
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

# User: List own contacts
@router.get("/contacts", response_model=List[ContactOut], tags=["user"])
async def list_my_contacts(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
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
