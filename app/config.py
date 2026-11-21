from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./todo_list.db"
    jwt_secret: str = "development-secret-change-me"
    jwt_expire_minutes: int = 120

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
