# Architecture

DDD + Clean Architecture + разделение ответственности.

Domain не зависит от FastAPI, SQLAlchemy, Telegram или Redis.

Application содержит use cases и orchestration.

Infrastructure содержит реализации БД и внешних сервисов.

Presentation содержит HTTP API и Telegram Bot adapters.

Development: SQLite + aiosqlite + SQLAlchemy async + greenlet.

Production: PostgreSQL + asyncpg + Redis.
