from dataclasses import dataclass


@dataclass
class RedisConnectionDTO:
    host: str
    port: int
    password: str
