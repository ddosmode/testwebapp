---
title: Архитектура проекта
---

# Архитектура проекта

## 1. Обзор архитектуры

!!! abstract "DDD + Clean Architecture"
    TestWebApp построен по принципам Domain-Driven Design и Clean Architecture.

    - **Domain** — бизнес-сущности и интерфейсы. Не зависит от FastAPI, SQLAlchemy, Redis или Telegram.
    - **Application** — use cases, сервисы и orchestration.
    - **Infrastructure** — реализации репозиториев, подключение к БД, Redis, Telegram, платежи.
    - **Presentation** — HTTP API и Telegram Bot адаптеры.

## 2. Слои

### Domain

Содержит:

- `entities.py` — бизнес-сущности (Product, Order, Cart и т.д.)
- `repositories.py` — интерфейсы репозиториев

Пример:

```python
class Product:
    id: UUID
    name: str
    price: Decimal
    is_active: bool

class ProductRepository(ABC):
    @abstractmethod
    async def list_products(self) -> list[Product]: ...
    
    @abstractmethod
    async def get_product(self, product_id: UUID) -> Product | None: ...
```

### Application

Содержит бизнес-логику:

- `services.py` — сервисы, реализующие use cases
- Связывает domain и infrastructure через Unit of Work

```python
class CatalogService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def list_products(self) -> list[Product]:
        async with self.uow as uow:
            return await uow.products.list()
```

### Infrastructure

Содержит технические реализации:

- `database/` — SQLAlchemy модели, репозитории, сессии, UoW
- `redis/` — работа с Redis
- `payments/` — интеграция с платежными системами
- `telegram/` — интеграция с Telegram

### Presentation

Содержит:

- `api/routes/` — FastAPI роутеры
- `bot/` — Telegram бот (точка входа подготовлена)

## 3. Разделение ответственности

| Слой          | Зависимости                    | Ответственность                  |
|---------------|--------------------------------|----------------------------------|
| Domain        | Только Python stdlib           | Бизнес-правила и сущности        |
| Application   | Domain, Infrastructure abstractions | Use cases и orchestration    |
| Infrastructure| External libraries (SQLAlchemy, Redis, aiogram) | Реализации |
| Presentation  | FastAPI, aiogram               | Входящие запросы и ответы        |

## 4. Преимущества подхода

- **Тестируемость**: Domain и Application не зависят от внешних фреймворков.
- **Гибкость**: Можно менять БД, фреймворк или способ доставки без изменения бизнес-логики.
- **Читаемость**: Четкое разделение на слои упрощает навигацию по коду.

После изучения архитектуры переходите к [бэкенду](backend.md).
