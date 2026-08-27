---
title: Docker
---

# Docker

## 1. Обзор

Docker используется для контейнеризации всех сервисов TestWebApp. Docker Compose описывает, как сервисы взаимодействуют между собой.

## 2. Файлы Compose

- `docker-compose.yml` — базовый файл с общими сервисами и сетью.
- `docker-compose.override.yml` — переопределения для development (порты, volumes, зависимости).
- `docker-compose.prod.yml` — дополнительные сервисы для продакшена (PostgreSQL, health checks).

## 3. Сервисы

### Backend

```yaml
backend:
  build:
    context: ./backend
    dockerfile: Dockerfile
  ports:
    - "8000:8000"
  environment:
    DATABASE_URL: ${DATABASE_URL}
    REDIS_URL: ${REDIS_URL:-redis://redis:6379/0}
    TELEGRAM_BOT_TOKEN: ${TELEGRAM_BOT_TOKEN}
    TELEGRAM_WEBAPP_URL: ${TELEGRAM_WEBAPP_URL}
    SECRET_KEY: ${SECRET_KEY}
  networks:
    - app-network
  restart: unless-stopped
```

### Frontend

```yaml
frontend:
  build:
    context: ./frontend
    dockerfile: Dockerfile
  ports:
    - "80:80"
  networks:
    - app-network
  restart: unless-stopped
```

### Redis

```yaml
redis:
  image: redis:7-alpine
  command: redis-server --appendonly yes
  volumes:
    - redis_data:/data
  healthcheck:
    test: ["CMD-SHELL", "redis-cli ping"]
    interval: 30s
    timeout: 10s
    start_period: 5s
    retries: 3
  networks:
    - app-network
  restart: unless-stopped
```

### PostgreSQL (продакшен)

```yaml
postgres:
  image: postgres:16-alpine
  environment:
    POSTGRES_USER: ${POSTGRES_USER:-app}
    POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    POSTGRES_DB: ${POSTGRES_DB:-app}
  volumes:
    - postgres_data:/var/lib/postgresql/data
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER:-app}"]
    interval: 30s
    timeout: 10s
    start_period: 5s
    retries: 3
  networks:
    - app-network
  restart: unless-stopped
```

## 4. Volumes

| Volume           | Назначение                                |
|------------------|-------------------------------------------|
| `redis_data`     | Персистентность Redis                     |
| `postgres_data`  | Данные PostgreSQL в продакшене            |
| `frontend_node_modules` | node_modules для разработки фронтенда |

## 5. Networks

Все сервисы общаются через сеть `app-network`:

- `backend` -> `postgres:5432`
- `backend` -> `redis:6379`
- `frontend` (nginx) -> `backend:8000` (проксируется)

## 6. Dockerfile бэкенда

Многоступенчатая сборка:

1. `builder` — создает venv и устанавливает зависимости.
2. `final` — копирует venv из builder, запускает приложение.

```dockerfile
FROM python:3.12-slim as builder
RUN python3 -m venv /venv && /venv/bin/pip install --upgrade pip wheel setuptools
COPY pyproject.toml /src/
COPY src /src/src
RUN /venv/bin/pip install '/src[bot]'

FROM python:3.12-slim
WORKDIR /src
COPY --from=builder /venv /venv
CMD ["/venv/bin/python", "-m", "app.main"]
```

## 7. Полезные команды

```bash
# Сборка
docker compose build

# Запуск
docker compose up

# Запуск с профилем продакшена
docker compose --profile prod up -d

# Логи
docker compose logs -f backend

# Остановка
docker compose down

# Выполнение команды в контейнере
docker compose exec backend bash
```

После изучения Docker переходите к [деплою](deployment.md).
