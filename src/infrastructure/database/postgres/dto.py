import typing as tp
from dataclasses import asdict, dataclass


@dataclass
class PostgresConnectionDTO:
    user: str
    host: str
    password: str
    database: str
    port: int = 5432

    def to_dict(self) -> tp.Self:
        return asdict(self)
