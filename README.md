# Веб-приложение "Список задач"

## Запуск проекта

### Локальный запуск для разработки

- Клонировать репозиторий 

```bash
git clone https://github.com/hazadus/fastapi-todos
cd fastapi-todos
```

- Создать файлы с настройками бэкенда и фронтенда

```bash
cp backend/.env.example backend/.env.dev
cp frontend/.env.example frontend/.env.dev
```

- Запустить проект в Docker

```bash
just dev
# или `docker compose --profile dev up`
```

- Применить миграции к БД (см. ниже)

- После запуска будут доступны:
   - Фронтенд на http://localhost:3000/
   - Бэкенда на http://localhost:8000/

#### Создание и применение миграций

```bash
# Запустить приложение в Докере
just dev
# Параллельно выполнить команду:
docker exec app-dev alembic revision --message="Add_some_new_table" --autogenerate
# Для применения миграций:
docker exec app-dev alembic upgrade head
```

## Документация 

- [Pinia](https://pinia.vuejs.org/)
- [VueUse](https://vueuse.org)