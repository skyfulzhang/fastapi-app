from typing import Any
from fastapi import APIRouter, Depends
from fastapi.requests import Request
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from database.database import get_db
from schemas.item import ItemInDB, ItemCreate, ItemUpdate
from core.custom_response import response_normal
from models.users import User
from core.util_tools import get_current_active_user
from crud.item import crud_item
from crud.user import crud_user
from core.custom_exception import ItemException, PermissionException, ServerException
from core.loguru_log import logger

router = APIRouter()


@router.get("/", )
async def read_items_multi(request: Request, skip: int = 0, limit: int = 10, db: Session = Depends(get_db),
                           current_user: User = Depends(get_current_active_user)) -> Any:
	try:
		if crud_user.is_superuser(current_user):
			items = crud_item.get_multi_items(db, skip=skip, limit=limit)
		else:
			items = crud_item.get_multi_by_owner(db=db, owner_id=current_user.id)
		req_info = {"url": request.url, "method": request.method, "headers": request.headers, "body": None,
		            "user": current_user.full_name}
		logger.info(f"Request:{req_info}")
		response = response_normal(data=jsonable_encoder(items))
		logger.info(f"Response:{jsonable_encoder(response.body)}")
		return response
	except Exception as e:
		logger.exception(e)
		raise ServerException()


@router.get("/{item_id}")
async def read_item_id(request: Request, item_id: int, db: Session = Depends(get_db),
                       current_user: User = Depends(get_current_active_user), ) -> Any:
	item = crud_item.get_item_by_id(db=db, id=item_id)
	req_data = {"item_id": item_id, "current_user": current_user.to_dict()}
	if not item:
		raise ItemException(req_data)
	if not crud_user.is_superuser(current_user) and (item.owner_id != current_user.id):
		raise PermissionException(req_data)
	req_info = {"url": request.url, "method": request.method, "headers": request.headers, "body": None,
	            "user": current_user.full_name}
	logger.info(f"Request:{req_info}")
	response = response_normal(data=jsonable_encoder(item))
	logger.info(f"Response:{jsonable_encoder(response.body)}")
	return response


@router.post("/")
async def create_item(request: Request, item_data: ItemCreate, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
	try:
		item = crud_item.create_with_owner(db=db, owner_id=current_user.id, item_obj=item_data)
		req_info = {"url": request.url, "method": request.method, "headers": request.headers,
		            "body": jsonable_encoder(item_data), "user": current_user.full_name}
		logger.error(f"Request:{req_info}")
		response = response_normal(data=jsonable_encoder(item))
		logger.info(f"Response:{jsonable_encoder(response.body)}")
		return response
	except Exception as e:
		logger.exception(e)
		raise ServerException()


@router.put("/{item_id}")
async def update_item(request: Request, item_id: int, item_in: ItemUpdate, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
	item = crud_item.get_item_by_id(db=db, id=item_id)
	req_data = {"item_id": item_id, "current_user": current_user.to_dict()}
	if not item:
		raise ItemException(req_data)
	if not crud_user.is_superuser(current_user) and (item.owner_id != current_user.id):
		raise PermissionException(req_data)
	try:
		item = crud_item.update_item(db=db, id=item_id, item_obj=item_in)
		body_data = await request.body()
		req_info = {"url": request.url, "method": request.method, "headers": request.headers, "body": body_data,
		            "user": current_user.full_name}
		logger.error(f"Request:{req_info}")
		response = response_normal(data=jsonable_encoder(item))
		logger.info(f"Response:{jsonable_encoder(response.body)}")
		return response
	except Exception as e:
		logger.exception(e)
		raise ServerException()


@router.delete("/{item_id}")
async def delete_item(request: Request, item_id: int, db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_active_user)):
	item = crud_item.get_item_by_id(db=db, id=item_id)
	req_data = {"item_id": item_id, "current_user": current_user.to_dict()}
	if not item:
		raise ItemException(req_data)
	if not crud_user.is_superuser(current_user) and (item.owner_id != current_user.id):
		raise PermissionException(req_data)
	req_info = {"url": request.url, "method": request.method, "headers": request.headers, "body": None,
	            "user": current_user.full_name}
	logger.error(f"Request:{req_info}")
	item = crud_item.delete_item(db=db, id=item_id)
	response = response_normal(data=jsonable_encoder(item))
	logger.info(f"Response:{jsonable_encoder(response.body)}")
	return response
