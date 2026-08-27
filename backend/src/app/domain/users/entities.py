from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class User:
    id: UUID
    telegram_id: int
    username: str | None = None
    is_admin: bool = False
    is_active: bool = True
