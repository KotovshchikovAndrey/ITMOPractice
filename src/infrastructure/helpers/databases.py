import typing as tp


def build_postgres_url(
    host: str,
    port: int,
    database: str,
    user: str,
    password: str,
) -> str:
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"
