import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    db_connection : str
    aws_role_arn: str
    aws_role_session_name: str

if __name__ == "__main__":
    config = AppConfig()