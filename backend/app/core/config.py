# app setting here
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)
from pydantic_core import MultiHostUrl
from pydantic import (
    computed_field,
    PostgresDsn,
)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore"
    ) # Pydantic .env support
    
    SECRET_KEY:str
    
    PROJECT_NAME:str
    
    # settings for db 
    DB_NAME:str
    DB_USER:str
    DB_PASSWORD:str
    DB_HOST:str
    DB_PORT:int
    
    # settings for mail
    MAIL_TLS:bool = True
    MAIL_SSL:bool = False
    MAIL_HOST:str
    MAIL_PORT:int = 587
    MAIL_USER:str
    MAIL_PASSWORD:str
    EMAILS_FROM_EMAIL:str|None=None
    
    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self)->PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=self.DB_NAME,
        )
    
    # settings for tokens
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 15 # change later
    REFRESH_TOKEN_EXPIRE_MINUTES:int = 60*24 # 1 day (change later)
    
    CRYPTCONTEXT_SCHEME:str = "bcrypt"
    
    ALGORITHM:str = "HS256"
    
settings = Settings()