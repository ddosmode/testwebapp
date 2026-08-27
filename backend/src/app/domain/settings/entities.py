from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True)
class Setting:
    id: UUID
    key: str
    value: str
