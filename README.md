# Веб-приложение "Список задач"

## Запуск проекта

### Локальный запуск для разработки

- Клонировать репозиторий 

```bash
git clone https://github.com/hazadus/fastapi-todos
cd fastapi-todos
```

- Создать файл с настройками бэкенда

```bash
cp backend/.env.example backend/.env.dev
```

- Запустить проект в Docker

```bash
just dev
# или `docker compose --profile dev up`
```

- Применить миграции к БД (см. ниже)

#### Создание и применение миграций

```bash
# Запустить приложение в Докере
just dev
# Параллельно выполнить команду:
docker exec app-dev alembic revision --message="Add_some_new_table" --autogenerate
# Для применения миграций:
docker exec app-dev alembic upgrade head
```
