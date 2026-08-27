---
title: База данных
---

# База данных

## 1. Обзор

TestWebApp использует:

- **SQLite + aiosqlite** в режиме разработки — не требует отдельного сервиса БД.
- **PostgreSQL 16** в продакшене — основная база данных.

Миграции управляются через **Alembic**.

## 2. Подключение

Строка подключения задается через переменную окружения `DATABASE_URL`:

```dotenv
# Development
DATABASE_URL=sqlite+aiosqlite:///./data/app.db

# Production
DATABASE_URL=postgresql+asyncpg://app:password@postgres:5432/app
```

## 3. Структура проекта базы данных

```
backend/src/app/infrastructure/database
├── base.py           # Базовые модели и миксины
├── models.py         # Экспорт моделей
├── models/           # Модели по доменам
├── repositories/     # Репозитории
├── session.py        # Фабрика сессий
└── uow.py            # Unit of Work
```

## 4. Модели

Модели определены с использованием SQLAlchemy 2.0 async:

```python
from sqlalchemy.orm import Mapped, mapped_column

class Product(Base, TableNameMixin):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    category_id: Mapped[UUID] = mapped_column(ForeignKey("categories.id"))
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[Optional[str]]
    price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2))
    is_active: Mapped[bool] = mapped_column(default=True)
```

## 5. Репозитории

Пример репозитория товаров:

```python
class ProductRepository(BaseRepo):
    async def list_products(self) -> list[Product]:
        stmt = select(Product).where(Product.is_active == True)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_product(self, product_id: UUID) -> Product | None:
        stmt = select(Product).where(Product.id == product_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
```

## 6. Unit of Work

```python
class SqlAlchemyUnitOfWork:
    async def __aenter__(self):
        self.session = session_factory()
        self.products = ProductRepository(self.session)
        self.categories = CategoryRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        if exc:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()
```

## 7. Миграции

```bash
# Создание миграции
alembic revision --autogenerate -m "description"

# Применение миграций
alembic upgrade head

# Откат
alembic downgrade -1
```

В Docker:

```bash
./scripts/migrate.sh prod
```

## 8. Данные для разработки

Файл SQLite создается автоматически при первом запуске в режиме разработки. Для наполнения тестовыми данными можно использовать скрипты или Alembic seed миграции.

После изучения базы данных переходите к [Docker](docker.md).
