import uuid
from typing import Optional
from pydantic import BaseModel, Field
from bson import ObjectId



class User(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    address: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    phone_number: Optional[str] = Field(None)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str,
        }
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "John.Doe@gmail.com",
                "address": "123 Street",
                "city": "New York",
                "phone_number": "1234567890",
            }
        }



class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None)
    last_name: Optional[str] = Field(None)
    email: Optional[str] = Field(None)
    address: Optional[str] = Field(None)
    city: Optional[str] = Field(None)
    phone_number: Optional[str] = Field(None)

    class Config:
        json_schema_extra = {
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "John.Doe@example.com",
                "address": "123 Street",
                "city": "New York",
                "phone_number": "1234567890",
            }
        }
