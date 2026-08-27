from abc import ABC, abstractmethod


class UnitOfWork(ABC):
    categories: object
    products: object
    inventory: object
    cities: object
    locations: object
    orders: object
    payment_methods: object
    payments: object
    users: object
    settings: object

    @abstractmethod
    async def __aenter__(self) -> "UnitOfWork":
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        raise NotImplementedError

    @abstractmethod
    async def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def rollback(self) -> None:
        raise NotImplementedError
