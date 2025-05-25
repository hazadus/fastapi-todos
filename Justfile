# Запустить проект в Докере в режиме разработки
dev:
    docker compose --profile dev up

# Запустить тесты бэкенда в Докере
test:
    docker compose run --rm app-test || true
    docker compose --profile test down --volumes
    docker image rm fastapi-todos-app-test
