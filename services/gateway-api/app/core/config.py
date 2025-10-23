from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    USERS_BASE_URL: str = "http://users-service:8000"
    TELEMETRY_BASE_URL: str = "http://telemetry-service:8000"
    AUDIT_BASE_URL: str = "http://audit-service:8000"
    JWT_SECRET: str = "change-me"
    JWT_ALG: str = "HS256"

settings = Settings()
