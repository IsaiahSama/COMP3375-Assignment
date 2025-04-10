from server.models.users import User
# from server.server import app
from dotenv import dotenv_values
from pymongo import MongoClient

config = dotenv_values(".env")
print(MongoClient(config["MONGO_URI"]))
# app.mongodb_client = MongoClient(config["MONGO_URI"])

async def get_user(user_id: int):
    pass

async def create_user(user: User):  
    pass

async def update_user(user_id: int, user: User):
    pass

async def delete_user(user_id: int):
    pass