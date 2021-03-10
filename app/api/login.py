from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from database.database import get_db
from crud.user import crud_user
from core.security import create_access_token
from core.custom_exception import InactiveException
from core.loguru_log import logger

router = APIRouter()


# swagger使用返回的响应为固定格式
@router.post("/login/access-token")
async def login_access_token(request: Request, db: Session = Depends(get_db),
                             form_data: OAuth2PasswordRequestForm = Depends()):
	user = crud_user.authenticate_user(db, email=form_data.username, password=form_data.password)
	if not crud_user.is_active(user):
		raise InactiveException({"form": form_data.__dict__})
	req_info = {"url": request.url, "method": request.method, "headers": request.headers, "form": form_data.__dict__}
	logger.info(f"Request:{req_info}")
	token = {"access_token": create_access_token(user.email), "token_type": "bearer"}
	logger.info(f"Response:{token}")
	return token


# 在其他前后端分离项目中使用，json格式
@router.post("/auth/token")
async def login_auth_token(request: Request, db: Session = Depends(get_db),
                           form_data: OAuth2PasswordRequestForm = Depends()):
	user = crud_user.authenticate_user(db, email=form_data.username, password=form_data.password)
	if not crud_user.is_active(user):
		raise InactiveException({"form": form_data.__dict__})
	req_info = {"url": request.url, "method": request.method, "headers": request.headers, "form": form_data.__dict__}
	logger.info(f"Request:{req_info}")
	token = create_access_token(user.email)
	data = {'code': 200, "success": True, 'message': None, 'data': None}
	data["data"] = {"Authorize": "bearer " + str(token)}
	logger.info(f"Response:{data}")
	return data
