from fastapi.responses import JSONResponse, Response
from typing import Union

Response_Success = {
	'code': 200,
	"success": True,
	'message': None,
	'data': None
}

Response_Failure = {
	'code': 999,
	"success": False,
	'message': None,
	'data': None

}


def response_normal(*, data: Union[list, dict, str]):
	data = JSONResponse(content={
		'code': 200,
		"success": True,
		'message': None,
		'data': data,
	})
	return data


def response_exception(*, data: Union[list, dict, str]):
	data = JSONResponse(content={
		'code': 999,
		"status": False,
		'message': None,
		'data': data
	})
	return data
