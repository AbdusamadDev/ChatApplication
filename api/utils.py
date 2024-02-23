from datetime import datetime, timezone, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import Union
import pytz
import os
import re

from database.manager import UserManager
from . import conf

password_context = CryptContext(schemes=["bcrypt"])


def get_unix_timestamp():
    # Get the current time in UTC timezone
    now_utc = datetime.now(pytz.utc)

    # Convert the current time to a Unix timestamp
    unix_timestamp = int(now_utc.timestamp())
    return unix_timestamp

def password_check(password):
    """
    Verify the strength of 'password'
    Returns a dict indicating the wrong criteria
    A password is considered strong if:
        8 characters length or more
        1 digit or more
        1 symbol or more
        1 uppercase letter or more
        1 lowercase letter or more
    """

    # defining the error messages
    errors = {
        "length_error": "Length should be 8 characters or more",
        "digit_error": "Should contain at least 1 digit",
        "uppercase_error": "Should contain at least 1 uppercase letter",
        "lowercase_error": "Should contain at least 1 lowercase letter",
        "symbol_error": "Should contain at least 1 symbol",
    }

    # initializing an empty dict for the errors
    error_dict = {}

    # calculating the length
    if len(password) < 8:
        error_dict["length_error"] = errors["length_error"]

    # searching for digits
    if re.search(r"\d", password) is None:
        error_dict["digit_error"] = errors["digit_error"]

    # searching for uppercase
    if re.search(r"[A-Z]", password) is None:
        error_dict["uppercase_error"] = errors["uppercase_error"]

    # searching for lowercase
    if re.search(r"[a-z]", password) is None:
        error_dict["lowercase_error"] = errors["lowercase_error"]

    # searching for symbols
    if re.search(r"[ !#$%&'()*+,-./[\\\]^_`{|}~" + r'"]', password) is None:
        error_dict["symbol_error"] = errors["symbol_error"]

    # return the error dict
    return error_dict


def authenticate(username, password):
    user = get_user(username=username)
    if user is None:
        return False
    db_password = user.get("password")
    return verify_password(password, db_password)


def hash_password(password):
    return password_context.hash(password)


def verify_password(password, hashed_password):
    return password_context.verify(password, hashed_password)


def get_user(username: str):
    model = UserManager()
    try:
        user = model.get(username=username)
        return user
    except AttributeError:
        return None


def create_access_token(data: dict):
    try:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=int(conf.EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, conf.SECRET_KEY, algorithm=conf.ALGORITHM)
        return encoded_jwt
    except JWTError:
        return None


def decode_token(token):
    try:
        algorithm = os.environ.get("ALGORITHM")
        secret_key = os.environ.get("SECRET_KEY")
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        return payload
    except JWTError:
        return {}


routes = lambda router: [route.path for route in router.routes]

if __name__ == "__main__":
    user = password_check("abdusamad")
    print(user)
