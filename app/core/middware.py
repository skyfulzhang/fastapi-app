import time
from fastapi import FastAPI, Request
from core.loguru_log import logger
from database.database import SessionLocal
from core.custom_exception import ServerException


# 中间件，获取请求时间
def register_middware(app: FastAPI):
	@app.middleware("http")
	async def add_process_time_header(request: Request, call_next):
		start_time = time.time()
		response = await call_next(request)
		process_time = time.time() - start_time
		response.headers["X-Process-Time"] = str(process_time)
		logger.info(f"Process-Time(s):{process_time}")
		return response

	# @app.middleware("http")
	# async def db_session_middleware(request: Request, call_next):
	# 	try:
	# 		request.state.db = SessionLocal()
	# 		response = await call_next(request)
	# 		return response
	# 	except Exception as e:
	# 		raise ServerException()
	# 	finally:
	# 		request.state.db.close()


"""
class AuthenticationMiddleware():
	def __init__(self, app: FastAPI, backend: AuthenticationBackend):
		self.app = app
		self.backend = backend

	async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
		conn = Request(scope)
		try:
			auth_result = await self.backend.authenticate(conn)
		except AuthenticationError as exc:
			return
		if auth_result is None:
			auth_result = AuthCredentials(), UnauthenticatedUser()
		# request.auth,request.user
		scope["auth"], scope["user"] = auth_result
		await self.app(scope, receive, send)


class AuthenticationBackend:
	async def authenticate(self, request: Request):
		if 'authorization' in request.headers and "bearer" in request.headers["authorization"] :
			token = request.headers["authorization"].split(" ")[-1]
			email = decode_token(token).get("sub")
			user = crud_user.get_by_email(db=session(), email=email)
			return token, user
		else:
			return

def decode_token(token):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		return payload
	except Exception as e:
		raise HTTPException(status_code=403)

"""
