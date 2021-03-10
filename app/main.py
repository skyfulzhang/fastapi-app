import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from database.database import SessionLocal

from api.api_router import api_router
from database.database import Base, engine
from core.util_tools import init_db
from core.custom_exception import register_exception
from core.middware import register_middware

# 创建app实例
app = FastAPI()

# 数据库引擎
Base.metadata.create_all(engine)

# 初始化数据库
init_db(SessionLocal())

# 跨域
origins = ["*"]

# 中间件
app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# 注册中间件
register_middware(app)

# 注册异常
register_exception(app)

# 添加蓝图
app.include_router(api_router, prefix="/api/v1")

if __name__ == '__main__':
	uvicorn.run('main:app', host="127.0.0.1", port=8090, reload=True, debug=True)
