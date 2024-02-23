import uuid


def get_unique_key() -> str:
    return str(uuid.uuid4())
