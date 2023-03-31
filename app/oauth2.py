from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import setting
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

Algorithm = setting.Algorithm
SECRET_KEY = setting.secret_key
jwt_token_expiration_time = int(setting.jwt_token_expiration_time)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=jwt_token_expiration_time)
    to_encode.update({"expire": expire.isoformat()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=Algorithm)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[Algorithm])
        id : str = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = schemas.Tokenid(id=id)
        return token_data

    except JWTError:
        raise credentials_exception


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                          detail=f"could not validate credentials",headers={"WWW-authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
