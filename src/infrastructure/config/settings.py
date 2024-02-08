from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    server_host: str
    server_port: int
    is_dev: bool

    postgresql_user: str
    postgresql_host: str
    postgresql_password: str
    postgresql_database: str
    postgresql_port: int

    memcached_host: str
    memcached_port: int

    api_prefix: str = "/api/v1"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
