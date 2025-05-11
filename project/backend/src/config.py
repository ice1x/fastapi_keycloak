from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    keycloak_url: str = "http://keycloak:8080"
    realm: str = "demo-realm"
    client_id: str = "frontend-client"
    algorithm: str = "RS256"
    frontend_url: str = "http://localhost:5173"

    cors_allow_origins: list[str] = [frontend_url]  # Можно переопределять в .env
    cors_allow_credentials: bool = True
    cors_allow_methods: list[str] = ["*"]
    cors_allow_headers: list[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env")


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
