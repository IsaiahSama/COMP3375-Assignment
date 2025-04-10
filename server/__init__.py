from dotenv import load_dotenv, dotenv_values
from os import getenv 

config = dotenv_values(".env") or dotenv_values("server/.env")

__all__ = ["config"]
