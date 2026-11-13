from datetime import datetime, timedelta, timezone
import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

ACCESS_TOKEN_SECRET_KEY = "WEvRjO6fnYKYpAu7jR8T41Tk93OyFvQ4rmmuQ7djuo7S2YQefabzrdoBhhfkwpvkmg3KFjIjnIXiq2xj6V3PlVMnMpV0FskbY17ofddm25cPfdH3rqcDq3KLsdxTL7C4bBvVuyQmCXKfGlBtHG8KakRrpNkNGHA6"
ACCESS_TOKEN_ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
resto_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/resto/login")

def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, ACCESS_TOKEN_SECRET_KEY, algorithm=ACCESS_TOKEN_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):    
    try:
        payload = jwt.decode(token, ACCESS_TOKEN_SECRET_KEY, algorithms=[ACCESS_TOKEN_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    account_type = payload.get("account_type")
    if account_type not in (None, "customer"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token account type",
            headers={"WWW-Authenticate": "Bearer"},
        )

    customer_id = payload.get("sub")
    if not isinstance(customer_id, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token subject",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return customer_id


def get_current_resto(token: str = Depends(resto_oauth2_scheme)) -> str:
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    resto_id = payload.get("sub")
    if payload.get("account_type") != "resto" or not isinstance(resto_id, str):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token subject",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return resto_id