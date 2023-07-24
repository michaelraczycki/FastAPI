from bson import ObjectId
from uuid import UUID

def transform_id(user):
    user['_id'] = str(user['_id'])
    return user

def to_python(value):
    if isinstance(value, ObjectId):
        return str(value)
    elif isinstance(value, UUID):
        return str(value)
    raise TypeError(f"Unable to serialize {type(value).__name__}")