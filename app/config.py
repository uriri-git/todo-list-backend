from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = "sqlite:///./todo_list.db"
    jwt_secret: str = "development-secret-change-me"
    jwt_expire_minutes: int = 120
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def origens_permitidas(self) -> tuple[str, ...]:
        """Endereços do front-end autorizados a chamar a API, a partir de CORS_ORIGINS.

        "a, b ,c," vira ("a", "b", "c"). É uma tupla: ninguém acrescenta origens depois que a API subiu.
        """
        return tuple(o.strip() for o in self.cors_origins.split(",") if o.strip())

settings = Settings()
