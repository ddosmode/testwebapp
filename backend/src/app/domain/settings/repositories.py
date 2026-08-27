from abc import ABC, abstractmethod

from .entities import Setting


class SettingsRepository(ABC):
    @abstractmethod
    async def get(self, key: str) -> Setting | None:
        raise NotImplementedError

    @abstractmethod
    async def set(self, setting: Setting) -> None:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, key: str) -> None:
        raise NotImplementedError
