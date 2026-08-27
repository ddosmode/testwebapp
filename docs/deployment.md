---
title: Deployment
---

# Deployment

## 1. Обзор

В этом разделе описаны способы деплоя TestWebApp: локальный режим разработки и продакшен на сервере.

## 2. Development

```bash
docker compose up
```

Использует:

- SQLite вместо PostgreSQL
- Redis в контейнере
- Hot reload для бэкенда и фронтенда

Сервисы:

- Frontend: http://localhost:5173
- Backend: http://localhost:8000

## 3. Production

```bash
./scripts/deploy.sh prod
```

Или:

```bash
docker compose --profile prod build
docker compose --profile prod run --rm backend alembic upgrade head
docker compose --profile prod up -d
```

Сервисы:

- Frontend: http://localhost (порт 80)
- Backend: http://localhost:8000
- PostgreSQL: порт 5432 (внутренний)
- Redis: порт 6379 (внутренний)

## 4. Миграции

```bash
./scripts/migrate.sh prod
```

## 5. Health Checks

| Сервис   | Проверка                        | Порт |
|----------|---------------------------------|------|
| Backend  | `GET /health`                   | 8000 |
| Frontend | HTTP 200 на корне               | 80   |
| PostgreSQL | `pg_isready`                  | 5432 |
| Redis    | `redis-cli ping`                | 6379 |

## 6. Volumes

| Volume          | Назначение                                |
|-----------------|-------------------------------------------|
| `postgres_data` | Данные PostgreSQL                         |
| `redis_data`    | Персистентность Redis (AOF)               |

## 7. Безопасность

- `.env` добавлен в `.gitignore` и никогда не должен коммититься.
- `SECRET_KEY` должен быть надежным случайным значением в продакшене.
- `TELEGRAM_BOT_TOKEN` должен храниться в секрете.
- В продакшене рекомендуется запускать контейнеры от не-root пользователя.

## 8. Troubleshooting

### Backend не может подключиться к БД

Убедитесь, что `DATABASE_URL` соответствует запущенной БД. В development используйте SQLite URL. В production — PostgreSQL URL с правильными учетными данными.

### Frontend показывает пустую страницу

Проверьте консоль браузера. Убедитесь, что бэкенд здоров и API прокси настроен правильно.

### Миграции не применяются

Убедитесь, что контейнер бэкенда запущен и `DATABASE_URL` указан верно. Проверьте логи:

```bash
docker compose logs backend
```

## 9. SSL/TLS

Завершайте TLS на обратном прокси (nginx, Caddy, cloud load balancer) перед контейнерами. При необходимости измените `frontend/nginx.conf` для кастомных заголовков или SSL настроек.
