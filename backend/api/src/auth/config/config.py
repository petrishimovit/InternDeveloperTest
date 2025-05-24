from authx import AuthX, AuthXConfig
# from config import config

authx_cfg = AuthX(config=AuthXConfig(
    JWT_ALGORITHM="HS256",
    JWT_SECRET_KEY="test",
    JWT_TOKEN_LOCATION=["cookies"],
    JWT_ACCESS_COOKIE_NAME="access_token" ,
    JWT_COOKIE_CSRF_PROTECT = False
      # Поддерживается в authx
))