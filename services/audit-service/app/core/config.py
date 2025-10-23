from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://admin:adminpassword@mongodb:27017/audit_db?authSource=admin"
    DB_NAME: str = "audit_db"

settings = Settings()
