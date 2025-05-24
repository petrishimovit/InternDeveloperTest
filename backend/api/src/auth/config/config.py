from authx import AuthX, AuthXConfig
from config import config

authx = AuthX(config=AuthXConfig(
    JWT_ALGORITHM="HS256",
    JWT_SECRET_KEY=config.JWT_SECRET_KEY,  # В .env
    JWT_TOKEN_LOCATION=["headers"],
))