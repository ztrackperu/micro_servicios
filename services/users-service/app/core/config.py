from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://admin:adminpassword@mongodb:27017/users_db?authSource=admin"
    DB_NAME: str = "users_db"

    JWT_SECRET: str = "change-me"
    JWT_ALG: str = "HS256"
    JWT_EXPIRE_MIN: int = 120

settings = Settings()
