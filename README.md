# Rest API

## Описание:
Реализация Rest API на базе фраймворка FastAPI.
Парсинг происходит с новостного портала [Rambler](https://www.rambler.ru/)

Так как rambler.ru активно блокирует подключение даже через Selenium автономности добиться с Rocketry не удалось.

## Локальный запуск:
1. Устанавливаем все зависимости:

        pip install requirements.txt -r
2. Запускаем наш парсер
    
        python parser.py
3. Запускаем приложение

        uvicorn main:app --reload
