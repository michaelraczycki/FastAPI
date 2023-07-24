from fastapi import FastAPI
from .utils.transformers import transform_id
from pymongo import MongoClient
from .routes import router
app = FastAPI()

import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file
mongo_connection_string = os.getenv("MONGO_CONNECTION_STRING")
mongo_database = os.getenv("MONGO_DATABASE_NAME")

@app.on_event("startup")
def startup_db_client():
    # Instantiate MongoDB connection
    app.mongodb_client = MongoClient(mongo_connection_string)
    app.database = app.mongodb_client[mongo_database]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    # Close MongoDB connection
    app.mongodb_client.close()

app.include_router(router, tags=["users"], prefix="/users")


@app.get("/")
async def read_root():
    return {"message": "Hello, MongoDB!",
            "current database is: " : app.database["name"],
            "collections in the db are: " : app.database.list_collection_names()}

@app.get("/users/list/{first_name}")
async def list_users(first_name: str):
    collection = app.database.get_collection("users")
    users = collection.find({"first_name": first_name})
    users_list = [transform_id(user) for user in users]
    return {"users": users_list}


@app.get("/users/{last_name}")
async def read_item(last_name: str):
    return {"item_id": last_name}

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the best user"}
