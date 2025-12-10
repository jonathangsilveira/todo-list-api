from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    auth_secret_key: str
    gen_salt_rounds: int = Field(default=9)

    local_db_url: str = Field(default="sqlite+aiosqlite:///db/todo_list.sqlite3")

    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_db: int = Field(default=0)

    debug_mode: bool = Field(default=False)

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )