from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://admin:adminpassword@mongodb:27017/telemetry_db?authSource=admin"
    DB_NAME: str = "telemetry_db"

settings = Settings()
