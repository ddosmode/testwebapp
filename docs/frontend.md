---
title: Frontend Development
---

# Frontend Development

## 1. Обзор

Frontend TestWebApp построен на React + TypeScript с использованием Vite. Приложение является Telegram Mini App и адаптируется под тему Telegram.

## 2. Стек технологий

- **React 18** — UI библиотека
- **TypeScript** — типизация
- **Vite** — сборщик и dev server
- **Tailwind CSS** — utility-first CSS фреймворк
- **React Router** — роутинг
- **Axios** — HTTP клиент

## 3. Структура проекта

```
frontend/src
├── App.tsx
├── main.tsx
├── vite-env.d.ts
├── index.css
├── entities/       # Бизнес-сущности
├── features/       # Фичи и бизнес-логика
├── widgets/        # Композитные компоненты
├── pages/          # Страницы приложения
├── shared/         # Переиспользуемые компоненты и утилиты
└── lib/            # Внешние интеграции и конфигурации
```

## 4. Роутинг

Маршруты определены в `App.tsx`:

```tsx
export const routes = [
  { path: "/", element: <CatalogPage /> },
  { path: "/product/:id", element: <ProductPage /> },
  { path: "/cart", element: <CartPage /> },
  { path: "/checkout", element: <CheckoutPage /> },
  { path: "/checkout/city", element: <CitySelectionPage /> },
  { path: "/checkout/payment", element: <PaymentMethodsPage /> },
  { path: "/orders", element: <OrdersPage /> },
  { path: "/orders/:id", element: <OrderTrackingPage /> },
  { path: "/legal", element: <LegalAcceptancePage /> },
  { path: "/documents", element: <DocumentsPage /> },
  { path: "/profile", element: <ProfilePage /> },
];
```

## 5. Переменные окружения

Файл `.env`:

```dotenv
VITE_API_URL=http://localhost:8000/api
VITE_TELEGRAM_BOT_TOKEN=
VITE_TELEGRAM_WEBAPP_URL=
```

Переменные с префиксом `VITE_` доступны в коде через `import.meta.env`.

## 6. API взаимодействие

Запросы к бэкенду выполняются через Axios. Пример из страницы каталога:

```tsx
const response = await axios.get(`${import.meta.env.VITE_API_URL}/catalog/products`);
```

## 7. Telegram WebApp

Интеграция с Telegram:

- Загрузка скрипта `https://telegram.org/js/telegram-web-app.js` в `index.html`.
- Использование `window.Telegram.WebApp` для адаптации интерфейса под тему Telegram.
- Возможность использования React-библиотек для Telegram WebApp.

## 8. Запуск

```bash
cd frontend
npm install
npm run dev
```

Dev server запустится на `http://localhost:5173`.

## 9. Сборка

```bash
npm run build
```

Собранные файлы попадают в `frontend/dist/` и монтируются в Nginx контейнер в продакшене.

После изучения фронтенда переходите к [базе данных](database.md).
