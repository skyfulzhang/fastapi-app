from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from database.database import get_db
from schemas.user import UserBase, UserCreate, UserUpdate
from models.users import User
from core.util_tools import get_current_active_superuser, get_current_active_user
from crud.user import crud_user
from core.custom_response import response_normal
from core.custom_exception import UserException, PermissionException, ExistException, ServerException
from core.loguru_log import logger

router = APIRouter()


def remove_key(dict_data, key):
	del dict_data[key]
	return dict_data


@router.get("/", )
async def read_users_multi(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_active_superuser)):
	try:
		users = crud_user.get_multi_users(db, skip=skip, limit=limit)
		user_data = jsonable_encoder(users)
		new_users = [remove_key(user, "hashed_password") for user in user_data]
		req_info = {"url": request.url, "method": request.method, "headers": request.headers, "body": None,
		            "user": current_user.full_name}
		logger.info(f"Request:{req_info}")
		response = response_normal(data=new_users)
		logger.info(f"Response:{jsonable_encoder(response.body)}")
		return response
	except Exception as e:
		logger.exception(e)
		raise ServerException()


@router.get("/me")
async def read_user_me(request: Request, current_user: User = Depends(get_current_active_superuser), ):
	req_info = {"url": request.url, "method": request.method, "headers": request.headers, "body": None,
	            "user": current_user.full_name}
	logger.info(f"Request:{req_info}")
	new_user = remove_key(jsonable_encoder(current_user), "hashed_password")
	response = response_normal(data=new_user)
	logger.info(f"Response:{jsonable_encoder(response.body)}")
	return response


@router.get("/{user_id}")
async def read_user_by_id(request: Request, user_id: int, db: Session = Depends(get_db),
                          current_user: User = Depends(get_current_active_superuser)):
	user = crud_user.get_user_by_id(db, id=user_id)
	req_data = {"user_id": user_id, "current_user": jsonable_encoder(current_user)}
	if not user:
		raise UserException(req_data)
	if not crud_user.is_superuser(current_user):
		raise PermissionException(req_data)
	req_info = {"url": request.url, "method": request.method, "headers": request.headers, "body": None,
	            "user": current_user.full_name}
	logger.info(f"Request:{req_info}")
	new_user = remove_key(jsonable_encoder(user), "hashed_password")
	response = response_normal(data=new_user)
	logger.info(f"Response:{jsonable_encoder(response.body)}")
	return response


@router.post("/")
async def create_user(request: Request, user_in: UserCreate, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_superuser), ):
	user = crud_user.get_user_by_email(db, email=user_in.email)
	req_data = {"user_in": jsonable_encoder(user_in), "current_user": jsonable_encoder(current_user)}
	if user:
		raise ExistException(req_data)
	try:
		user = crud_user.create_user(db, user_obj=user_in)
		new_user = remove_key(jsonable_encoder(user), "hashed_password")
		req_info = {"url": request.url, "method": request.method, "headers": request.headers,
		            "body": jsonable_encoder(user_in), "user": current_user.full_name}
		logger.info(f"Request:{req_info}")
		response = response_normal(data=new_user)
		logger.info(f"Response:{jsonable_encoder(response.body)}")
		return response
	except Exception as e:
		logger.exception(e)
		raise ServerException()


@router.put("/me")
async def update_user_me(request: Request, user_in: UserBase, db: Session = Depends(get_db),
                         current_user: User = Depends(get_current_active_superuser)):
	try:
		user = crud_user.update_user(db, user_old=current_user, user_in=user_in)
		print("hello")
		new_user = remove_key(jsonable_encoder(user), "hashed_password")
		req_info = {"url": request.url, "method": request.method, "headers": request.headers,
		            "body": jsonable_encoder(user_in), "user": current_user.full_name}
		logger.info(f"Request:{req_info}")
		response = response_normal(data=new_user)
		logger.info(f"Response:{jsonable_encoder(response.body)}")
		return response
	except Exception as e:
		logger.exception(e)
		raise ServerException()


@router.put("/{user_id}")
async def update_user(request: Request, user_id: int, user_in: UserUpdate, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_superuser), ):
	user = crud_user.get_user_by_id(db, id=user_id)
	req_data = {"user_id": user_id, "current_user": jsonable_encoder(current_user)}
	if not user:
		raise UserException(req_data)
	if not crud_user.is_superuser(current_user):
		raise PermissionException(req_data)
	try:
		user = crud_user.update_user(db, user_old=user, user_in=user_in)
		new_user = remove_key(jsonable_encoder(user), "hashed_password")
		req_info = {"url": request.url, "method": request.method, "headers": request.headers,
		            "body": jsonable_encoder(user_in), "user": current_user.full_name}
		logger.info(f"Request:{req_info}")
		response = response_normal(data=jsonable_encoder(new_user))
		logger.info(f"Response:{jsonable_encoder(response.body)}")
		return response
	except Exception as e:
		logger.exception(e)
		raise ServerException()
