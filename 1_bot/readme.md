
# Price Tracking Bot

Этот проект представляет собой Telegram-бота для отслеживания цен на товары с платформы Яндекс.Маркет. Пользователи могут добавлять ссылки на товары, просматривать историю изменений цен и удалять отслеживаемые товары.

## Как работает бот

1. **Добавление товара для отслеживания**: Отправьте боту ссылку на товар с Яндекс.Маркет.
2. **Просмотр истории цен**: Используйте команду `/history <количество дней>`, чтобы увидеть историю изменения цен за указанный период.
3. **Удаление товара**: Удалите товар из отслеживаемых, отправив команду `/delete <id_предмета>`.

Бот автоматически проверяет цены на добавленные товары каждые 10 минут и обновляет их в базе данных.

---

## Установка и запуск

### Шаг 1: Клонирование репозитория

Склонируйте проект с помощью команды:

```bash
git clone <URL репозитория>
cd <имя папки проекта>
```

### Шаг 2: Настройка окружения

1. Убедитесь, что у вас установлен Python (рекомендуется версия 3.8 или выше).
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```
3. Настройте переменные окружения:
   - `BOT_TOKEN`: токен вашего Telegram-бота.
   - `DATABASE_URL`: URL вашей PostgreSQL базы данных.

### Шаг 3: Настройка базы данных

Создайте таблицу в базе данных с помощью SQL-запроса:

```sql
CREATE TABLE price_tracking (
    id SERIAL PRIMARY KEY,
    user_id BIGINT NOT NULL,
    item_name TEXT NOT NULL,
    item_url TEXT NOT NULL,
    current_price NUMERIC NOT NULL,
    price_history JSONB NOT NULL DEFAULT '[]'::jsonb,
    last_checked TIMESTAMP DEFAULT NOW()
);
```

### Шаг 4: Запуск бота

Запустите бота командой:

```bash
python bot.py
```

---

## Используемые технологии

- **aiogram**: библиотека для работы с Telegram Bot API.
- **PostgreSQL**: база данных для хранения информации о товарах и их ценах.
- **BeautifulSoup**: для парсинга данных с Яндекс.Маркет.

---

## Основные файлы

- **bot.py**: основной файл, реализующий команды бота и логику обработки сообщений.
- **db_manager.py**: модуль для взаимодействия с базой данных.
- **parser.py**: модуль для парсинга цен и названий товаров с Яндекс.Маркет.
