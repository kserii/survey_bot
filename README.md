# Телеграм бот для опросов

## Установка
Нужен Docker (в идеале version 25.0.3, build 4debf41) и Docker Compose (version v2.24.5).

Перед сборкой нужно переименовать файл `.env.example` в `.env`.
В нем указать актуальные значения для:
- `BOT_TOKEN`. Ключ-токен для телеграм бота, получить у @BotFather

Собираем образ:
```shell
git clone ...
cd survey_bot
docker-compose -f docker-compose.prod.yml up --build -d
```

Все должно работать.
