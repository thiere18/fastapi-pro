# from jose import JWTError, jwt
from datetime import datetime, timedelta

from jose import JWTError,jwt
from . import schemas, database,models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')
from  .config import settings as st

# SECRET_KEY
# Algorithm
# Expriation time
oauth2_scheme=OAuth2PasswordBearer(tokenUrl='login')
SECRET_KEY = st.secret_key
ALGORITHM = st.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = st.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt
def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,ALGORITHM)
        id:str =payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data=schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token:str = Depends(oauth2_scheme),db:Session =Depends(database.get_db)):
    credentials_exception=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
    detail=f"could not validate credentials",headers={"WWW-Authenticate":"Bearer"})
    token=verify_access_token(token,credentials_exception)
    user=db.query(models.User).filter(models.User.id ==token.id).first()
    return user




    