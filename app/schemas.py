

from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List


class ContactBase(BaseModel):
	name: str
	email: Optional[EmailStr] = None
	phone: Optional[str] = None
	address: Optional[str] = None

	@field_validator('name')
	def name_must_not_be_empty(cls, v):
		if not v or not v.strip():
			raise ValueError('Name must not be empty')
		return v

	@field_validator('phone')
	def phone_length(cls, v):
		if v and (len(v) < 7 or len(v) > 15):
			raise ValueError('Phone number must be between 7 and 15 digits')
		return v

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
