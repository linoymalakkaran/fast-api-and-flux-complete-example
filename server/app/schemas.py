from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional, List

# UserCreate schema for creating users
class UserCreate(BaseModel):
	username: str
	password: str
	role: str
	class Config:
		schema_extra = {
			"example": {
				"username": "user1",
				"password": "password123",
				"role": "user"
			}
		}

class ContactBase(BaseModel):
	name: str = "John Doe"
	email: Optional[EmailStr] = "john@example.com"
	phone: Optional[str] = "+1234567890"
	address: Optional[str] = "123 Main St"

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
	class Config:
		schema_extra = {
			"example": {
				"name": "John Doe",
				"email": "john@example.com",
				"phone": "+1234567890",
				"address": "123 Main St"
			}
		}

class ContactUpdate(ContactBase):
	pass
	class Config:
		schema_extra = {
			"example": {
				"name": "Jane Doe",
				"email": "jane@example.com",
				"phone": "+1987654321",
				"address": "456 Elm St"
			}
		}

class ContactOut(ContactBase):
	id: int = 1
	user_id: int = 1
	class Config:
		orm_mode = True
		schema_extra = {
			"example": {
				"id": 1,
				"user_id": 1,
				"name": "John Doe",
				"email": "john@example.com",
				"phone": "+1234567890",
				"address": "123 Main St"
			}
		}

class UserOut(BaseModel):
	id: int = 1
	username: str = "user1"
	role: str = "user"
	class Config:
		schema_extra = {
			"example": {
				"id": 1,
				"username": "user1",
				"role": "user"
			}
		}
	contacts: List[ContactOut] = []
	class Config:
		orm_mode = True
