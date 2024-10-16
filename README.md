# CDNVideoTZ

## Описание
cdnvideotz — это проект, предоставляющий API на базе FastAPI с документацией Swagger. Использует PostgreSQL в качестве базы данных и Docker для удобного развёртывания.

### Требования
- Docker
- Docker Compose

### Установка и запуск

1. Склонируйте репозиторий:
    ```
    git clone https://github.com/axem4n31/CDNVideoTZ.git
    cd cdnvideotz
    ```
2. Создайте файл .env в корневой директории и укажите следующие переменные окружения:
    ```
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=123123
    POSTGRES_HOST=db
    POSTGRES_DB=postgres
    WEATHER_API_TOKEN=52279adb38b340d8829133744240606
    ```
3. Запустите приложение с помощью Docker::
    ```
    docker-compose up --build
    ```
4. После успешного развёртывания перейдите по адресу http://localhost:8080/docs для доступа к Swagger UI.

### Использование
- Для взаимодействия с API используйте Swagger UI по адресу http://localhost:8080/docs, где вы сможете тестировать все доступные эндпоинты.

### Остановка
Для остановки приложения используйте:
```
docker-compose down
```

### Примечания
- Убедитесь, что порты 8080 (для FastAPI) и 5432 (для PostgreSQL) не заняты другими приложениями на вашем компьютере.
- Для изменения порта доступа к приложению, отредактируйте файл docker-compose.yml и укажите другой порт в секции ports.

### Контакты
- Автор: Топоров Денис
- Email: toporov.axeman@gmail.com
- Telegram: @axem4n