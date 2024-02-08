from dataclasses import dataclass


@dataclass
class PostgresConnectionDTO:
    user: str
    host: str
    password: str
    database: str
    port: int = 5432
