from enum import IntEnum

"""
from enum import IntEnum

__all__ = ['ExceptionEnum']


class ExceptionEnum(IntEnum):
	def __new__(cls, value, phrase, ):
		obj = int.__new__(cls, value)
		obj._value_ = value
		obj.phrase = phrase
		return obj

	BAD_REQUEST = (400, 'Bad Request',)
	UNAUTHORIZED = (401, 'Unauthorized',)
	PAYMENT_REQUIRED = (402, 'Payment Required',)
	FORBIDDEN = (403, 'Forbidden',)
	NOT_FOUND = (404, 'Not Found',)
	METHOD_NOT_ALLOWED = (405, 'Method Not Allowed',)
	NOT_ACCEPTABLE = (406, 'Not Acceptable',)
	PROXY_AUTHENTICATION_REQUIRED = (407, 'Proxy Authentication Required',)
	REQUEST_TIMEOUT = (408, 'Request Timeout',)
	CONFLICT = (409, 'Conflict',)


value = ExceptionEnum.BAD_REQUEST.value
phrase = ExceptionEnum.BAD_REQUEST.phrase
print(value)
print(phrase)


"""


# 异常枚举中，code必须不一样
class ExceptionEnum(IntEnum):
	def __new__(cls, value, phrase, ):
		obj = int.__new__(cls, value)
		obj._value_ = value
		obj.phrase = phrase
		return obj

	TOKEN_EXPIRED = (4001, 'token expire!',)
	AUTH_FAILED = (4007, 'auth failed!',)
	USERNAME_PASSWORD = (4000, 'username or password incorrect!',)
	INACTIVE_USER = (4003, 'user not active!',)
	USER_NOT_FOUND = (4004, 'user not found!',)
	USER_NO_PERMISSION = (4002, 'user no permission!',)
	USER_ALREADY_EXIST = (4005, 'user already exist!',)
	ITEM_NOT_FOUND = (4006, 'item not found!',)
	SERVER_ERROR = (5000, 'internal server error!',)
