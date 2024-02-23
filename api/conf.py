import os


SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")
EXPIRE_MINUTES = os.environ.get("EXPIRE_MINUTES")
