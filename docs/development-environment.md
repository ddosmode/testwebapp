---
title: Локальный деплой
---

# Локальный деплой (Development)

В этом разделе описано, как запустить TestWebApp на локальной машине для разработки и тестирования.

## 1. Обзор режимов запуска

Проект поддерживает два режима:

- **Development**: быстрая локальная разработка с автоматической перезагрузкой кода.
- **Production**: продакшен запуск через Docker Compose с PostgreSQL и Redis.

Для локальной разработки рекомендуется использовать `docker-compose.override.yml`, который автоматически подключается при запуске `docker compose up`.

## 2. Запуск через Docker Compose

### Базовая команда

```bash
docker compose up
```

Эта команда:

1. Собирает образы бэкенда и фронтенда.
2. Запускает Redis.
3. Запускает бэкенд на порту `8000`.
4. Запускает фронтенд на порту `5173`.

### Доступные сервисы

| Сервис   | URL                    | Описание                          |
|----------|------------------------|-----------------------------------|
| Frontend | http://localhost:5173  | React + TypeScript приложение     |
| Backend  | http://localhost:8000  | FastAPI REST API                  |
| Redis    | localhost:6379         | Кэш и сессии                      |

### Health Check

```bash
curl http://localhost:8000/health
```

## 3. Переменные окружения

В режиме разработки по умолчанию используется SQLite. Файл базы данных создается автоматически в `backend/data/app.db`.

Переменные окружения подтягиваются из `.env` в корне проекта. Если файл отсутствует, создайте его:

```bash
cp .env.example .env
```

Минимальный набор для разработки:

```dotenv
APP_ENV=development
DEBUG=true
SECRET_KEY=dev-secret-key
DATABASE_URL=sqlite+aiosqlite:///./data/app.db
REDIS_URL=redis://redis:6379/0
TELEGRAM_BOT_TOKEN=
TELEGRAM_WEBAPP_URL=http://localhost:5173
```

## 4. Volumes и hot reload

`docker-compose.override.yml` подключает:

- `./backend/src:/app/src` — изменения в Python коде сразу доступны в контейнере.
- `./frontend:/app` и `frontend_node_modules:/app/node_modules` — для разработки фронтенда.

## 5. Остановка сервисов

```bash
docker compose down
```

Данные SQLite сохраняются в `backend/data/app.db`. Если нужно удалить их:

```bash
rm backend/data/app.db
```

## 6. Проверка работоспособности

```bash
# Health
curl http://localhost:8000/health

# Catalog
curl http://localhost:8000/api/catalog/products
```

После успешного локального запуска переходите к [продакшен деплою](production-environment.md) или [запуску приложения](running.md).
