from typing import Optional, Any
from pydantic import BaseModel

base_response = {
	"code": 200,
	"success": True,
	"msg": None,
	"data": None
}


class Response(BaseModel):
	code: int
	msg: Optional[str]
	success: bool
	data: Optional[Any]


class BaseResponse(BaseModel):
	code: int
	msg: str
	success: bool
	data: Any
