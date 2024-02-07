from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    server_host: str
    server_port: int
    is_dev: bool

    postgres_user: str
    postgres_host: str
    postgres_port: int
    postgres_password: str
    postgres_database: str

    memcached_host: str
    memcached_port: int

    api_prefix: str = "/api/v1"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
