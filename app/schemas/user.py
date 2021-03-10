from typing import Optional

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
	full_name: str
	email: EmailStr


class UserCreate(UserBase):
	password: str
	is_active: bool = True
	is_superuser: bool = False


class UserUpdate(UserBase):
	password: Optional[str] = None
	is_active: bool = True


class UserInDB(UserBase):
	id: int

	class Config:
		orm_mode = True
