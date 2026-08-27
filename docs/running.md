---
title: Запуск приложения
---

# Запуск приложения

После настройки конфигурации и зависимостей пришло время запустить TestWebApp.

## 1. Предварительная проверка

Убедитесь, что:

- `.env` создан и заполнен.
- Docker и Docker Compose установлены.
- Порт `8000` и `5173` свободны (в режиме разработки).

```bash
docker compose ps
```

## 2. Локальный запуск

```bash
docker compose up
```

Сервисы станут доступны:

- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Health: http://localhost:8000/health

## 3. Продакшен запуск

```bash
./scripts/deploy.sh prod
```

Или вручную:

```bash
docker compose --profile prod build
docker compose --profile prod run --rm backend alembic upgrade head
docker compose --profile prod up -d
```

## 4. Миграции базы данных

```bash
./scripts/migrate.sh prod
```

## 5. Проверка работоспособности

```bash
# Backend
curl http://localhost:8000/health

# Catalog API
curl http://localhost:8000/api/catalog/products

# Frontend
curl -I http://localhost:5173
```

## 6. Остановка

```bash
docker compose down
```

## 7. Просмотр логов

```bash
docker compose logs -f backend
docker compose logs -f frontend
```

## 8. Использование приложения

1. Откройте фронтенд в браузере.
2. Или откройте Telegram, найдите вашего бота и нажмите кнопку WebApp.

После запуска приложения переходите к изучению [архитектуры проекта](architecture.md).
