from dotenv import dotenv_values

config = dotenv_values(".env")

TOKEN = config.get("TOKEN")

DB_NAME = config.get("DB_NAME")
DB_USER = config.get("DB_USER")
DB_PASSWORD = config.get("DB_PASSWORD")
DB_HOST = config.get("DB_HOST")
DB_PORT = config.get("DB_PORT")
