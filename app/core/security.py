from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

# 密钥，不可泄露
SECRET_KEY = "BmNR93ztupJMVeDjd2CXPmCckGzJRccdi0VQVTK_Pdc"
# import secrets
# SECRET_KEY = secrets.token_urlsafe(32)
# 加密算法
ALGORITHM = "HS256"
# 过期时间，单位分钟
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(sub: str, expires_delta: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
	expire = datetime.utcnow() + timedelta(seconds=expires_delta)
	token_encode = ({"sub": sub, "exp": expire})
	encoded_jwt = jwt.encode(token_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
	return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
	return pwd_context.hash(password)


def decode_token(token):
	decode_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
	print(decode_token)
	return decode_token
