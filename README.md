# DUCK'S GameClub Telegram Bot

Telegram-бот для пользователей DUCK'S GameClub на Python 3.11+, `aiogram 3` и REST API backend.

Бот не обращается к базе данных напрямую. Все клубные данные берутся только через `API_BASE_URL`.

## Возможности

- `/start` — главное меню.
- `/help` — список команд.
- `/events` — ближайшие опубликованные мероприятия.
- `/poker`, `/darts`, `/billiards` — фильтр мероприятий по игре.
- Запись на мероприятие через inline-кнопку `Записаться`.
- `/rating` — рейтинг игроков по игре.
- `/rules` — правила клуба.
- `/feedback` — отправка сообщения клубу.
- `/link <backend_user_id>` — локальная привязка Telegram user к backend user id.

## Переменные окружения

Скопируйте пример и заполните токен:

```bash
cp .env.example .env
```

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
API_BASE_URL=http://localhost:4000/api
API_TIMEOUT_SECONDS=10
LOG_LEVEL=INFO
USER_LINKS_PATH=data/user_links.json
```

`/link` хранит связь `telegram_user_id -> backend_user_id` в локальном JSON-файле. Для production не доверяйте произвольному `backend_user_id`: лучше добавить backend endpoint или одноразовый код подтверждения.

## Локальный запуск

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python -m main
```

Backend должен быть доступен по `API_BASE_URL`, например `http://localhost:4000/api`.

## Тесты

```bash
pip install -e ".[dev]"
pytest
```

## Docker

```bash
docker build -t ducks-telegram-bot .
docker run --env-file .env -v ducks_bot_data:/app/data ducks-telegram-bot
```

## Архитектура

```text
src/
  main.py
  config/settings.py
  bot/
    callbacks.py
    factory.py
    formatters.py
    keyboards.py
  api/
    client.py
    errors.py
    models.py
  handlers/
    start.py
    events.py
    ratings.py
    rules.py
    feedback.py
    linking.py
  state/feedback.py
  storage/user_links.py
  logging_config/setup.py
tests/
```

HTTP-запросы идут через `ApiClient` на `httpx.AsyncClient` с timeout. Безопасные `GET`-запросы ретраятся, `POST`-запросы не ретраятся. Ошибки backend формата `{ "error": { "code": "...", "message": "...", "details": {} } }` логируются, пользователю показываются короткие сообщения.
