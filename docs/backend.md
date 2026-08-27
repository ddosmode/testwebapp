---
title: Backend API
---

# Backend API

## 1. Введение

!!! abstract "Обзор"
    Этот раздел описывает архитектуру бэкенда TestWebApp, принципы организации кода и ключевые сервисы.

!!! warning "Требования"
    - Перед изучением бэкенда убедитесь, что у вас установлены Docker и Docker Compose.
    - Желательно familiarity с Python и FastAPI.

## 2. Архитектура

Проект построен по принципам DDD и Clean Architecture:

- **Domain**: бизнес-сущности и интерфейсы репозиториев. Не зависит от FastAPI, SQLAlchemy, Redis или Telegram.
- **Application**: use cases, сервисы и orchestration.
- **Infrastructure**: реализации репозиториев, работа с БД, Redis, Telegram, платежами.
- **Presentation**: HTTP API и адаптеры для Telegram Bot.

Структура директории `backend/src/app`:

```
backend/src/app
├── domain/
│   ├── catalog/
│   ├── inventory/
│   ├── locations/
│   ├── orders/
│   ├── payments/
│   ├── settings/
│   ├── shared/
│   └── users/
├── application/
│   ├── catalog/
│   ├── inventory/
│   ├── locations/
│   ├── orders/
│   ├── payments/
│   ├── settings/
│   ├── telegram/
│   └── users/
├── infrastructure/
│   ├── database/
│   ├── payments/
│   ├── redis/
│   └── telegram/
└── presentation/
    ├── api/
    └── bot/
```

## 3. REST API

### Entry Point

`backend/src/app/main.py` экспортирует FastAPI приложение из `presentation/api`.

### Организация API

API разделено на routers по доменам:

- `auth.py` — аутентификация
- `catalog.py` — каталог товаров и категорий
- `cart.py` — корзина
- `checkout.py` — оформление заказа
- `cities.py` — города
- `orders.py` — заказы
- `payments.py` — платежи
- `health.py` — health check

Каждый router имеет префикс и теги:

```python
router = APIRouter(prefix="/catalog", tags=["catalog"])
```

### Пример endpoints

**Список товаров:**

```python
@router.get("/products")
async def list_products() -> list[dict[str, object]]:
    service = get_catalog_service()
    products = await service.list_products()
    return [...]
```

**Получение товара по ID:**

```python
@router.get("/products/{product_id}")
async def get_product(product_id: UUID) -> dict[str, object]:
    service = get_catalog_service()
    product = await service.get_product(product_id)
    return {...}
```

### Конфигурация

Переменные окружения загружаются через `pydantic-settings` в `backend/src/app/config/settings.py`.

## 4. Доменные сервисы

### CatalogService

Отвечает за бизнес-логику работы с каталогом:

```python
class CatalogService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def list_products(self) -> list[Product]:
        async with self.uow as uow:
            return await uow.categories.list_products()

    async def get_product(self, product_id: UUID) -> Product:
        async with self.uow as uow:
            return await uow.categories.get_product(product_id)
```

### Unit of Work

`SqlAlchemyUnitOfWork` обеспечивает единую транзакционную границу и exposes репозитории:

```python
class SqlAlchemyUnitOfWork:
    def __init__(self, session_factory: SessionFactory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()
        self.categories = CategoryRepository(self.session)
        self.products = ProductRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
```

## 5. Telegram Bot

Точка входа для Telegram бота подготовлена в `presentation/bot/`. Дальнейшая реализация зависит от требований к боту.

## 6. Запуск API

### Через Docker

```bash
docker compose up backend
```

### Локально

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

После изучения бэкенда переходите к [фронтенду](frontend.md).
