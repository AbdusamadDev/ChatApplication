from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI, HTTPException

from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from typing import Annotated, Union
from jose import jwt, JWTError
from pydantic import BaseModel

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
HTTP_401_UNAUTHORIZED = 401
password_context = CryptContext(schemes=["bcrypt"])
fake_db = {}


class User(BaseModel):
    username: str
    password: str


class TokenData(BaseModel):
    token: str
    token_type: str


def hash_password(password):
    return password_context.hash(password)


def verify_password(password, hashed_password):
    return password_context.verify(password, hashed_password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=60)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, "asdasdasdasd", algorithm="HS256")
        return encoded_jwt
    except JWTError:
        return None


def get_user():
    pass


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, "asdasdasdasd", ["HS256"])
    except JWTError:
        raise credentials_exception
    user = get_user()
    if user is None:
        raise credentials_exception


def authenticate(username, password):
    for i in fake_db.values():
        if username == i["username"]:
            return verify_password(password, i["password"])
    return False


@app.post("/token")
async def get_token(data: User):
    username, password = data.username, data.password
    user = authenticate(username, password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    expire_date = datetime.now() + timedelta(minutes=0)
    access_token = create_access_token({"user": username, "exp": expire_date})
    return TokenData(token=access_token, token_type="bearer")


@app.post("/create_user")
async def create_new_user(user: User):
    username = user.username
    password = user.password
    fake_db[username] = {"username": username, "password": hash_password(password)}
    return fake_db[username]


@app.get("/items/")
async def read_items():
    pass
