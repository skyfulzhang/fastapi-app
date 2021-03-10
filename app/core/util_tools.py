import jwt
from jwt import PyJWTError
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from database.database import get_db
from models.users import User
from schemas.user import UserCreate
from crud.user import crud_user
from core.security import SECRET_KEY, ALGORITHM
from core.custom_exception import TokenException, AuthException, UserException
from core.custom_exception import InactiveException, PermissionException
from core.loguru_log import logger

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")

FIRST_SUPERUSER = {
	"full_name": "skyful zhang",
	"email": "skyful@163.com",
	"password": "skyful123456"
}


def init_db(db: Session) -> None:
	user = crud_user.get_user_by_email(db, email=FIRST_SUPERUSER.get("email"))
	if not user:
		user_in = UserCreate(
			full_name=FIRST_SUPERUSER.get("full_name"),
			email=FIRST_SUPERUSER.get("email"),
			password=FIRST_SUPERUSER.get("password"),
			is_superuser=True,
		)
		user = crud_user.create_user(db, obj_in=user_in)
		logger.info("Initial data create success")
		logger.info(str(user.to_dict()))


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
	req_data = {"token": token}
	try:
		decode_jwt = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		email = decode_jwt.get("sub")
		expire = decode_jwt.get("exp")
	except PyJWTError:
		raise AuthException(req_data)
	else:
		if (email is None) or (expire is None):
			raise AuthException(req_data)
		user = crud_user.get_user_by_email(db, email=email)
		if not user:
			raise UserException(req_data)
		if datetime.fromtimestamp(expire) < datetime.utcnow():
			raise TokenException(req_data)
		return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
	if not crud_user.is_active(current_user):
		raise InactiveException({"current_user":current_user.to_dict()})
	return current_user


def get_current_active_superuser(current_user: User = Depends(get_current_user)) -> User:
	if not crud_user.is_superuser(current_user):
		raise PermissionException({"current_user":current_user.to_dict()})
	return current_user



