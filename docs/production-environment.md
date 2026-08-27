---
title: Продакшен деплой
---

# Продакшен деплой (Production)

В этом разделе описано, как запустить TestWebApp в продакшене на сервере.

## 1. Требования

- **Сервер** с Linux.
- **Домен**, указывающий на сервер.
- **SSL сертификат** (рекомендуется Let's Encrypt Certbot).
- **Docker и Docker Compose** установлены на сервере.

## 2. Переменные окружения

Создайте `.env` на сервере на основе `.env.example`:

```dotenv
APP_ENV=production
DEBUG=false
SECRET_KEY=<надежный случайный ключ>

DATABASE_URL=postgresql+asyncpg://app:password@postgres:5432/app
REDIS_URL=redis://redis:6379/0

TELEGRAM_BOT_TOKEN=<токен бота>
TELEGRAM_WEBAPP_URL=https://ваш-домен.ru

POSTGRES_USER=app
POSTGRES_PASSWORD=<пароль>
POSTGRES_DB=app
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
```

## 3. Запуск

```bash
docker compose --profile prod up -d
```

Профиль `prod` подключает PostgreSQL, включает production зависимости и запускает все сервисы с рестартом `unless-stopped`.

## 4. Сервисы в продакшене

| Сервис     | Порт      | Описание                            |
|------------|-----------|-------------------------------------|
| Frontend   | 80        | Nginx, отдает статику фронтенда     |
| Backend    | 8000      | FastAPI REST API                    |
| PostgreSQL | 5432      | Основная база данных                |
| Redis      | 6379      | Кэш и сессии                        |

## 5. Миграции

```bash
./scripts/migrate.sh prod
```

Или через Docker Compose:

```bash
docker compose --profile prod run --rm backend alembic upgrade head
```

## 6. Полный деплой

```bash
./scripts/deploy.sh prod
```

Скрипт выполняет:

1. Сборку образов.
2. Применение миграций.
3. Запуск сервисов.
4. Ожидание готовности health checks.

## 7. Nginx

В режиме продакшена фронтенд раздается через Nginx. При необходимости измените `frontend/nginx.conf` для кастомных заголовков или SSL.

TLS лучше завершать на внешнем reverse proxy (nginx, Caddy, cloud load balancer).

## 8. Безопасность

- Никогда не коммитьте `.env` в репозиторий.
- Используйте надежный `SECRET_KEY` в продакшене.
- Храните `TELEGRAM_BOT_TOKEN` в секрете.
- Ограничьте доступ к портам базы данных и Redis только внутренней сетью Docker.

После успешного деплоя переходите к [запуску приложения](running.md).
