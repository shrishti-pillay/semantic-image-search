import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file = os.getenv("ENV_FILE", ".env"),
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="forbid",
    )
    db_connection : str
    aws_role_arn: str
    aws_role_session_name: str

if __name__ == "__main__":
    config = AppConfig()