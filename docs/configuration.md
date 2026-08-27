---
title: Настройка конфигурации
---

# Настройка конфигурации

Прежде чем запустить ваш экземпляр TestWebApp и бота, вам нужно клонировать репозиторий и настроить несколько конфигурационных файлов.

## 1. Предварительные шаги

1. Клонируйте репозиторий проекта

    ```bash
    git clone https://github.com/testwebapp-cf1f9e2fe875.git
    ```

2. Перейдите в директорию проекта

    ```bash
    cd testwebapp
    ```

## 2. Получение домена и SSL сертификата

- Если вы запускаете локально, можно использовать настройку Ngrok для получения домена и SSL сертификата. [Прочтите раздел о настройке Ngrok](ngrok.md).
- Если вы запускаете на сервере, можно использовать домен, который уже принадлежит вам. [Прочтите раздел о получении домена](owned-domain.md).

После того как у вас есть домен и SSL сертификат, запишите домен(ы) для следующего шага.

## 3. Конфигурация бота и базы данных

1. Переименуйте файл `.env.example` в `.env`.
    
    ```bash
    mv .env.example .env
    ```

2. Откройте содержимое `.env`:
    Откройте с помощью nano/vim:
    ```bash
    nano .env
    ```

3. Внутри `.env` измените следующие переменные:

    ```dotenv hl_lines="1 2 5 6 10" title=".env"
    APP_ENV=development
    DEBUG=true
    SECRET_KEY=change-me-in-production

    DATABASE_URL=sqlite+aiosqlite:///./data/app.db
    # DATABASE_URL=postgresql+asyncpg://app:password@postgres:5432/app

    REDIS_URL=redis://redis:6379/0

    TELEGRAM_BOT_TOKEN=
    TELEGRAM_WEBAPP_URL=
    ```

4. Обновите `SECRET_KEY` на безопасное случайное значение. Для генерации можно использовать:
    ```bash
    python -c "import secrets; print(secrets.token_urlsafe(32))"
    ```
5. Укажите `TELEGRAM_BOT_TOKEN` — токен вашего Telegram бота, полученный у [@BotFather](https://t.me/BotFather).
6. Укажите `TELEGRAM_WEBAPP_URL` — адрес, по которому будет доступен фронтенд.
7. Настройте `DATABASE_URL`:
    - Для локальной разработки используйте SQLite по умолчанию: `sqlite+aiosqlite:///./data/app.db`
    - Для продакшена используйте PostgreSQL: `postgresql+asyncpg://app:password@postgres:5432/app`
8. При необходимости измените `REDIS_URL`, если вы используете внешний Redis.

## 4. Конфигурация фронтенда

1. Перейдите в директорию фронтенда и переименуйте файл `.env.example` в `.env`.
    
    ```bash
    cd frontend
    mv .env.example .env
    ```

2. Откройте содержимое `.env`:
    Откройте с помощью nano/vim:
    ```bash
    nano .env
    ```
    Вы должны увидеть:
    ```dotenv title="frontend/.env"
    VITE_API_URL=http://localhost:8000/api
    VITE_TELEGRAM_BOT_TOKEN=
    VITE_TELEGRAM_WEBAPP_URL=
    ```

3. Обновите переменные:

    - `VITE_API_URL` — адрес бэкенда. В продакшене это обычно тот же домен, что и у фронтенда (nginx проксирует запросы).
    - `VITE_TELEGRAM_BOT_TOKEN` — токен Telegram бота.
    - `VITE_TELEGRAM_WEBAPP_URL` — URL вашего Telegram WebApp.

!!! success "Готово!"

    Вы успешно настроили проект. Перейдите к [следующему шагу — инициализации зависимостей](dependencies-initialization.md).
