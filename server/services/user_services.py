from server.models.users import User
# from server.server import app
from server import config
from pymongo import MongoClient

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
