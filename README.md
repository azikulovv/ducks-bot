# DUCK'S Telegram Bot

Production-ready Telegram-бот игрового клуба DUCK'S на Python 3.11+, `python-telegram-bot` и SQLite.

## Возможности

- `/events` — будущие мероприятия с фильтром по покеру, дартсу и бильярду.
- Запись на событие через inline-кнопку с защитой от повторной записи.
- Автоматическая регистрация пользователей при первом контакте.
- `/ratingpoker`, `/ratingdart`, `/ratingbill` — рейтинги по участию.
- `/rules`, `/support`, `/feedback`.
- Админ-команды через whitelist `ADMIN_IDS`.
- Напоминания участникам примерно за 24 часа до события.

## Админ-команды

- `/admin_add_event` — пошаговое создание мероприятия.
- `/admin_events` — список активных будущих мероприятий с ID.
- `/admin_delete_event <event_id>` — мягкое удаление мероприятия.
- `/admin_registrations <event_id>` — список записавшихся пользователей.

## Локальный запуск Linux/macOS

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Заполните `.env`: `BOT_TOKEN`, `ADMIN_IDS`, при необходимости `ADMIN_CHAT_ID`.

```bash
python bot.py
```

## Локальный запуск Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Заполните `.env`, затем:

```powershell
python bot.py
```

## Docker

```bash
docker build -t ducks-telegram-bot .
docker run --env-file .env -v ducks_bot_data:/app/data ducks-telegram-bot
```

## Render

1. Создайте новый `Worker` из репозитория.
2. Выберите Docker runtime или используйте `render.yaml`.
3. Добавьте переменные окружения из `.env.example`.
4. Для SQLite подключите persistent disk и выставьте `DATABASE_PATH` в путь на диске, например `/var/data/ducks_bot.sqlite3`.
5. Запустите deploy. Бот работает в polling mode, web service не нужен.

## Railway

1. Создайте проект из GitHub-репозитория.
2. Добавьте переменные окружения из `.env.example`.
3. Укажите start command: `python bot.py`.
4. Подключите volume и задайте `DATABASE_PATH` на путь volume, чтобы SQLite не терялась при рестартах.

## Heroku

1. Добавьте `Procfile`.
2. Создайте приложение и задайте config vars:

```bash
heroku config:set BOT_TOKEN=... ADMIN_IDS=... ADMIN_CHAT_ID=...
```

3. Включите worker:

```bash
heroku ps:scale worker=1
```

SQLite на Heroku ephemeral filesystem не подходит для долгого production-хранения. Для Heroku используйте внешний volume-совместимый хостинг или перенесите БД на managed SQL.
