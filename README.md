# Веб-приложение "Список задач"

## Запуск проекта

Для управления проектом используется инструмент [just](https://just.systems/man/en/). Необходимо его [установить](https://just.systems/man/en/packages.html), чтобы не выполнять команды из [Justfile](./Justfile) вручную.

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

#### Тесты бэкенда

1. Тесты запускаются в Докере при помощи команды `just test`. При этом, каждый раз создаётся чистая база данных для интеграционных тестов.
2. Файл настроек приложения для тестов `./backend/.env.test` редактировать не требуется.


## Документация 

- [Pinia](https://pinia.vuejs.org/)
- [VueUse](https://vueuse.org)