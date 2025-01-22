from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from typing import Optional
from dotenv import load_dotenv
import os 
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: Optional[str] = Field(default="",description="The project name") 
    DATABASE_URL:  str = os.environ.get("DATABASE_URL","")
    DATABASE_NAME: str = os.environ.get("DATABASE_NAME")

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore"
    )

settings = Settings() # type: ignore