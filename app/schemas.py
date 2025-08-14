
from pydantic import BaseModel
from typing import Optional, List

class ContactBase(BaseModel):
	name: str
	email: Optional[str] = None
	phone: Optional[str] = None
	address: Optional[str] = None

class ContactCreate(ContactBase):
	pass

class ContactUpdate(ContactBase):
	pass

class ContactOut(ContactBase):
	id: int
	user_id: int
	class Config:
		orm_mode = True

class UserOut(BaseModel):
	id: int
	username: str
	role: str
	contacts: List[ContactOut] = []
	class Config:
		orm_mode = True
