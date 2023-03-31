from pydantic import BaseSettings


class Settings(BaseSettings):
    database_host: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    Algorithm: str
    secret_key: str
    jwt_token_expiration_time: str

    class Config:
        env_file = ".env"


setting = Settings()
