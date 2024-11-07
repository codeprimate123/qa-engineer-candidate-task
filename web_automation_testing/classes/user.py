from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    username: str
    first_name: str
    last_name: str
    zip_code: str
