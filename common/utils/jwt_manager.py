from datetime import datetime, timedelta, timezone
from jose import jwt

def create_access_token(data: dict, secret: str, algorithm: str, expire_minutes: int) -> str:
    to_encode = data.copy()
    expire = datetime.now(tz=timezone.utc) + timedelta(minutes=expire_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret, algorithm=algorithm)

def decode_token(token: str, secret: str, algorithms: list[str]) -> dict:
    return jwt.decode(token, secret, algorithms=algorithms)
