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
