from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError,ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Union

from core.exception_enum import ExceptionEnum
from core.loguru_log import logger


class UnicornException(Exception):
	def __init__(self, msg: str = None):
		self.msg = msg


class LoginException(Exception):
	def __init__(self, body):
		self.body = body
		self.code = ExceptionEnum.USERNAME_PASSWORD.value
		self.msg = ExceptionEnum.USERNAME_PASSWORD.phrase


class TokenException(Exception):
	def __init__(self, body):
		self.body = body
		self.code = ExceptionEnum.TOKEN_EXPIRED.value
		self.msg = ExceptionEnum.TOKEN_EXPIRED.phrase


class AuthException(Exception):
	def __init__(self, body):
		self.body = body
		self.code = ExceptionEnum.AUTH_FAILED.value
		self.msg = ExceptionEnum.AUTH_FAILED.phrase


class InactiveException(Exception):
	def __init__(self, body):
		self.body = body
		self.code = ExceptionEnum.INACTIVE_USER.value
		self.msg = ExceptionEnum.INACTIVE_USER.phrase


class UserException(Exception):
	def __init__(self, body):
		self.body = body
		self.code = ExceptionEnum.USER_NOT_FOUND.value
		self.msg = ExceptionEnum.USER_NOT_FOUND.phrase


class ItemException(Exception):
	def __init__(self, body):
		self.body = body
		self.code = ExceptionEnum.ITEM_NOT_FOUND.value
		self.msg = ExceptionEnum.ITEM_NOT_FOUND.phrase


class PermissionException(Exception):
	def __init__(self, body):
		self.body = body
		self.code = ExceptionEnum.USER_NO_PERMISSION.value
		self.msg = ExceptionEnum.USER_NO_PERMISSION.phrase


class ExistException(Exception):
	def __init__(self, body):
		self.body = body
		self.code = ExceptionEnum.USER_ALREADY_EXIST.value
		self.msg = ExceptionEnum.USER_ALREADY_EXIST.phrase


class ServerException(Exception):
	def __init__(self):
		self.code = ExceptionEnum.SERVER_ERROR.value
		self.msg = ExceptionEnum.SERVER_ERROR.phrase


def register_exception(app: FastAPI) -> None:
	# 请求异常，定义好就行，不用管
	@app.exception_handler(RequestValidationError)
	async def validation_exception_handler(request: Request, exc: Union[RequestValidationError, ValidationError]):
		req_info = {"url": request.url, "method": request.method, "headers": request.headers,
		            "body": str(exc.body)}
		logger.error(f"Request:{req_info}")
		data = {"code": 400, "success": False, "msg": str(exc.errors()), "data": {"body": str(exc.body)}}
		logger.error(f"Response:{data}")
		return JSONResponse(content=data, status_code=400)

	# 响应异常,exc的值来自HTTPException的status_code和detail
	@app.exception_handler(StarletteHTTPException)
	async def http_exception_handler(request: Request, exc: StarletteHTTPException):
		body_data = await request.body()
		req_info = {"url": request.url, "method": request.method, "headers": request.headers, "body": body_data}
		logger.error(f"Request:{req_info}")
		data = {"code": exc.status_code, "msg": str(exc.detail), "success": False, "data": None}
		logger.error(f"Response:{data}")
		return JSONResponse(content=data, status_code=exc.status_code)

	# 自定义异常，代码中抛出
	@app.exception_handler(UnicornException)
	async def unicorn_exception_handler(request: Request, exc: UnicornException):
		body_data = await request.body()
		req_info = {"url": request.url, "method": request.method, "headers": request.headers, "body": body_data}
		logger.error(f"Request:{req_info}")
		data = {"code": 999, "success": False, "msg": str(exc.msg), "data": None}
		logger.error(f"Response:{data}")
		return JSONResponse(content=data, status_code=400)

	# 登录异常
	@app.exception_handler(LoginException)
	async def login_exception_handler(request: Request, exc: LoginException):
		req_info = {"url": request.url, "method": request.method, "headers": request.headers, "body": exc.body}
		logger.error(f"Request:{req_info}")
		data = {"code": exc.code, "success": False, "msg": str(exc.msg), "data": None}
		logger.error(f"Response:{data}")
		return JSONResponse(content=data, status_code=400)

	# token过期
	@app.exception_handler(TokenException)
	async def token_exception_handler(request: Request, exc: TokenException):
		req_info = {"url": request.url, "method": request.method, "headers": request.headers, "body": exc.body}
		logger.error(f"Request:{req_info}")
		data = {"code": exc.code, "success": False, "msg": str(exc.msg), "data": None}
		logger.error(f"Response:{data}")
		return JSONResponse(content=data, status_code=400)

	# 认证失败
	@app.exception_handler(AuthException)
	async def auth_exception_handler(request: Request, exc: AuthException):
		req_info = {"url": request.url, "method": request.method, "headers": request.headers, "body": exc.body}
		logger.error(f"Request:{req_info}")
		data = {"code": exc.code, "success": False, "msg": str(exc.msg), "data": None}
		logger.error(f"Response:{data}")
		return JSONResponse(content=data, status_code=400)

	# 未激活异常
	@app.exception_handler(InactiveException)
	async def inactive_exception_handler(request: Request, exc: InactiveException):
		req_info = {"url": request.url, "method": request.method, "headers": request.headers, "body": exc.body}
		logger.error(f"Request:{req_info}")
		data = {"code": exc.code, "success": False, "msg": str(exc.msg), "data": None}
		logger.error(f"Response:{data}")
		return JSONResponse(content=data, status_code=400)

	# User不存在
	@app.exception_handler(UserException)
	async def user_exception_handler(request: Request, exc: UserException):
		req_info = {"url": request.url, "method": request.method, "headers": request.headers, "body": exc.body}
		logger.error(f"Request:{req_info}")
		data = {"code": exc.code, "success": False, "msg": str(exc.msg), "data": None}
		logger.error(f"Response:{data}")
		return JSONResponse(content=data, status_code=400)

	# Item不存在
	@app.exception_handler(ItemException)
	async def item_exception_handler(request: Request, exc: ItemException):
		req_info = {"url": request.url, "method": request.method, "headers": request.headers, "body": exc.body}
		logger.error(f"Request:{req_info}")
		data = {"code": exc.code, "success": False, "msg": str(exc.msg), "data": None}
		logger.error(f"Response:{data}")
		return JSONResponse(content=data, status_code=400)

	# 权限异常
	@app.exception_handler(PermissionException)
	async def permission_exception_handler(request: Request, exc: PermissionException):
		req_info = {"url": request.url, "method": request.method, "headers": request.headers, "body": exc.body}
		logger.error(f"Request:{req_info}")
		data = {"code": exc.code, "success": False, "msg": str(exc.msg), "data": None}
		logger.error(f"Response:{data}")
		return JSONResponse(content=data, status_code=400)

	# 用户已存在
	@app.exception_handler(ExistException)
	async def exist_exception_handler(request: Request, exc: ExistException):
		req_info = {"url": request.url, "method": request.method, "headers": request.headers, "body": exc.body}
		logger.error(f"Request:{req_info}")
		data = {"code": exc.code, "success": False, "msg": str(exc.msg), "data": None}
		logger.error(f"Response:{data}")
		return JSONResponse(content=data, status_code=400)

	# 服务器异常，except 中抛出
	@app.exception_handler(ServerException)
	async def server_exception_handler(request: Request, exc: ServerException):
		body_data = await request.body()
		req_info = {"url": request.url, "method": request.method, "headers": request.headers, "body": body_data}
		logger.error(f"Request:{req_info}")
		data = {"code": 1001, "success": False, "msg": "服务器内部错误", "data": None}
		logger.error(f"Response:{data}")
		return JSONResponse(content=data, status_code=502)
