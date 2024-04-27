# Телеграм бот для опросов

## Установка
Нужен Docker (в идеале version 25.0.3, build 4debf41) и Docker Compose (version v2.24.5).

Перед сборкой нужно переименовать файл `.env.example` в `.env`.
В нем указать актуальные значения для:
- `BOT_TOKEN`. Ключ-токен для телеграм бота, получить у @BotFather

Собираем образ:
```shell
cd survey_bot
docker-compose build .
docker-compose up -d
```

Все должно работать.

## Проблемы

О ошибках сообщайте по почте: konstantin.serez@gmail.com
