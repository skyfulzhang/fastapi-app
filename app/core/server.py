from fastapi import FastAPI, Request
from fastapi.middleware import Middleware

def create_app() -> FastAPI:
	"""生成FatAPI对象"""
	app = FastAPI()

	# 跨域设置
	register_cors(app)

	# 注册路由
	register_router(app)

	# 注册捕获全局异常
	# register_exception(app)

	# 请求中间件
	register_middware(app)

	# fastapi初始化
	register_init(app)

	return app


def register_cors(app: FastAPI):
	from fastapi.middleware.cors import CORSMiddleware
	app.add_middleware(
		CORSMiddleware,
		allow_origins=["*"],
		allow_credentials=True,
		allow_methods=["*"],
		allow_headers=["*"],
	)


def register_router(app: FastAPI):
	app.include_router()


def register_middware(app: FastAPI):
	import time
	@app.middleware("http")
	async def add_process_time_header(request: Request, call_next):
		start_time = time.time()
		response = await call_next(request)
		process_time = time.time() - start_time
		response.headers["X-Process-Time"] = str(process_time)
		return response


def register_init(app: FastAPI) -> None:
	"""初始化连接"""

	@app.on_event("startup")
	async def init_connect():
		# 连接redis
		# redis.connect()
		# 初始化 apscheduler
		# schedule.init_scheduler()
		print("startup")

	@app.on_event('shutdown')
	async def close_connect():
		# redis.close()
		# schedule.shutdown()
		print("shutdown")
