"""Configuration management for the Census Data Agent."""

from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):    
    db_host: str = Field(
        default="localhost",
        env="DB_HOST"
    )
    
    db_port: int = Field(
        default=5432,
        env="DB_PORT"
    )
    
    db_name: str = Field(
        default="data_agent",
        env="DB_NAME"
    )
    
    db_user: str = Field(
        default="postgres",
        env="DB_USER"
    )
    
    db_password: str = Field(
        default="postgres",
        env="DB_PASSWORD"
    )
    
    db_read_only_user: str = Field(
        default="census_reader",
        env="DB_READ_ONLY_USER"
    )
    
    db_read_only_password: str = Field(
        default="readonly_password",
        env="DB_READ_ONLY_PASSWORD"
    )
    
    anthropic_api_key: Optional[str] = Field(
        default=None,
        env="ANTHROPIC_API_KEY"
    )
    
    log_level: str = Field(
        default="INFO",
        env="LOG_LEVEL"
    )
    
    class Config:
        env_file = "../.env"
        case_sensitive = False
        extra = "allow"


settings = Settings()
