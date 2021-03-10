from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from core.security import hash_password, verify_password
from models.users import User
from schemas.user import UserCreate, UserUpdate
from core.custom_exception import LoginException, UserException, ServerException


class CrudUser():
	def get_user_by_id(self, db: Session, id: int) -> Optional[User]:
		return db.query(User).filter(User.id == id).first()

	def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
		return db.query(User).filter(User.email == email).first()

	def get_multi_users(self, db: Session, skip: int = 0, limit: int = 100) -> Optional[User]:
		return db.query(User).offset(skip).limit(limit).all()

	def create_user(self, db: Session, user_obj: UserCreate) -> User:
		try:
			hashed_password = hash_password(user_obj.password)
			user_data = jsonable_encoder(user_obj)
			del user_data["password"]
			db_obj = User(**user_data, hashed_password=hashed_password)
			db.add(db_obj)
			db.commit()
			db.refresh(db_obj)
			return db_obj
		except Exception as e:
			db.rollback()
			raise ServerException()

	def update_user(self, db: Session, user_old: User, user_in: UserUpdate) -> User:
		try:
			user_data = jsonable_encoder(user_old)
			update_data = user_in.dict(exclude_unset=True)
			if update_data.get("password"):
				update_data["hashed_password"] = hash_password(update_data["password"])
			for field in user_data:
				if field in update_data:
					setattr(user_old, field, update_data[field])
			db.add(user_old)
			db.commit()
			db.refresh(user_old)
			return user_data
		except Exception as e:
			db.rollback()
			raise ServerException()

	def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
		user = self.get_user_by_email(db, email=email)
		req_data = {"email": email, "password": password}
		if (not user) or (not verify_password(password, user.hashed_password)):
			raise LoginException(req_data)
		return user

	def is_active(self, user: User) -> bool:
		return user.is_active

	def is_superuser(self, user: User) -> bool:
		return user.is_superuser


crud_user = CrudUser()
