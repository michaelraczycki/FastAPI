from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from typing import List
from .utils.transformers import to_python

from app.models.user import User, UserUpdate

router = APIRouter()


@router.post("/", response_description="Add new user", status_code=status.HTTP_201_CREATED, response_model=User)
def create_user(request: Request, user: User = Body(...)):
    user_dict = user.dict(by_alias=True)  # Convert User model to dictionary
    new_user = request.app.database["users"].insert_one(user_dict)
    created_user = request.app.database["users"].find_one({"_id": new_user.inserted_id})
    return created_user

@router.get("/", response_description="List all users", response_model=List[dict])
def list_users(request: Request):
    users = list(request.app.database["users"].find(limit=100))
    for user in users:
        user['_id'] = to_python(user['_id'])
    return users

@router.get("/{user_id}", response_description="Get a single user", response_model=User)
def find_user(user_id: str, request: Request):
    if (user := request.app.database["users"].find_one({"_id": user_id})) is not None:
        return user
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")

@router.put("/{user_id}", response_description="Update a user", response_model=User)
def update_user(user_id: str, request: Request, user: UserUpdate = Body(...)):
    user = {k: v for k, v in user.dict().items() if v is not None}
    if len(user) >= 1:
        update_result = request.app.database["users"].update_one({"_id": user_id}, {"$set": user})
        if update_result.modified_count == 1:
            if (
                updated_user := request.app.database["users"].find_one({"_id": user_id})
            ) is not None:
                return updated_user
    if (existing_user := request.app.database["users"].find_one({"_id": user_id})) is not None:
        return existing_user
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")

@router.delete("/{user_id}", response_description="Delete a user")
def delete_user(user_id: str, request: Request):
    delete_result = request.app.database["users"].delete_one({"_id": user_id})
    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"User {user_id} not found")