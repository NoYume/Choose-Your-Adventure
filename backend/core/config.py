from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import field_validator
import os

class Settings(BaseSettings):
    API_PREFIX: str = "/api"
    DEBUG: bool = False
    DATABASE_URL: Optional[str] = None
    ALLOWED_ORIGINS: str = ""
    ANTHROPIC_API_KEY: Optional[str] = None
    
    
    def __init__(self, **values):
        super().__init__(**values)

        raw_url = os.getenv("POSTGRES_URL") or os.getenv("DATABASE_URL")
        
        if raw_url:
            self.DATABASE_URL = raw_url.replace("postgres://", "postgresql://", 1)
        
        if not self.DATABASE_URL:
            db_user = os.getenv("POSTGRES_USER")
            db_password = os.getenv("POSTGRES_PASSWORD") 
            db_host = os.getenv("POSTGRES_HOST")
            db_port = "5432"
            db_name = os.getenv("POSTGRES_DATABASE")
            if all([db_user, db_password, db_host, db_port, db_name]):
                self.DATABASE_URL = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


    @field_validator("ALLOWED_ORIGINS")
    def parse_allowed_origins(cls, v: str) -> List[str]:
        return v.split(",") if v else []


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()