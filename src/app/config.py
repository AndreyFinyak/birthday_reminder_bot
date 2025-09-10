from pydantic import BaseSettings


class Settings(BaseSettings):
    bot_token: str = ""
    database_path: str = "birthdays.db"
    timezone: str = "UTC"

    class Config:
        env_file = ".env"

    @classmethod
    def load(cls):
        return cls()
