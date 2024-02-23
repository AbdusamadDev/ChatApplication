from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.exc import IntegrityError
from fastapi.security import OAuth2PasswordBearer

from database.manager import UserManager
from .. import status, conf
from .serializers import (
    User,
    TokenData,
    UserRegistration,
    UserInfo,
    MessageResponse,
)
from ..utils import (
    create_access_token,
    password_check,
    hash_password,
    authenticate,
    get_user,
)

from jose.exceptions import ExpiredSignatureError
from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
router = APIRouter(prefix="/auth")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, conf.SECRET_KEY, [conf.ALGORITHM])
        token = token.split(" ")[-1]
        username: str = payload.get("user")
        if username is None:
            raise credentials_exception
    except ExpiredSignatureError:
        credentials_exception.detail = "Token expired or invalid"
        raise credentials_exception
    except JWTError:
        raise credentials_exception
    print("Username: ", username)
    user = get_user(username=username)
    if user is None:
        raise credentials_exception
    return user


@router.post("/token", response_model=TokenData)
async def get_token(data: User):
    user = authenticate(data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication credentials failed!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    expire_date = datetime.utcnow() + timedelta(minutes=int(conf.EXPIRE_MINUTES))
    access_token = create_access_token({"user": data.username, "exp": expire_date})
    return TokenData(token=access_token, token_type="bearer")


@router.post("/register", response_model=MessageResponse)
async def create_user(payload: UserRegistration):
    try:
        user = UserManager()
        pwd_check = password_check(payload.password)
        if pwd_check:
            raise HTTPException(
                detail=pwd_check,
                status_code=status.HTTP_400_BAD_REQUEST,
            )
        user.add(
            username=payload.username,
            email=payload.email,
            password=hash_password(payload.password),
        )
        return MessageResponse(
            message="User created successfully!", status_code=status.HTTP_201_CREATED
        )
    except IntegrityError:
        raise HTTPException(
            detail=f"User {payload.username, payload.email} already exists!",
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@router.get("/me", response_model=UserInfo)
async def get_me(user=Depends(get_current_user)):
    user.pop("password", None)
    return user
