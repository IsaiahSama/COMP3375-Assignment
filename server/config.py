from dotenv import load_dotenv, dotenv_values
from os import getenv

env_loaded = load_dotenv()

if not env_loaded:
    print("Could not find dotenv in current folder")
    load_dotenv("server/.env", verbose=True)


class Configuration:
    password: str | None
    username: str | None
    mongo_uri: str | None
    mongo_db_name: str | None

    def __init__(self):
        self.password = getenv("PASSWORD")
        self.username = getenv("USERNAME")
        self.mongo_uri = getenv("MONGO_URI")
        self.mongo_db_name = getenv("MONGO_DB_NAME")

        if not all([self.password, self.username, self.mongo_uri, self.mongo_db_name]):
            raise SystemError(f"Could not get all values from dotenv")


config = Configuration()
