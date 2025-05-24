import logfire
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.v1.auth import router as auth_router
from app.api.v1.tasks import router as tasks_router
from app.core.config import settings
from app.schemas import HealthcheckResponseSchema

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=[
        "GET",
        "POST",
        "OPTIONS",
        "DELETE",
        "PATCH",
        "PUT",
    ],
)

for router in [
    auth_router,
    tasks_router,
]:
    app.include_router(router=router, prefix="/api/v1")

logfire.configure(
    send_to_logfire="if-token-present",
    token=settings.LOGFIRE_TOKEN or None,
    service_name=settings.LOGFIRE_SERVICE_NAME,
    console=False,
)
logfire.instrument_fastapi(
    app=app,
    capture_headers=True,
)

# Настраиваем инструментатор Prometheus для сбора метрик
instrumentator = Instrumentator(
    should_group_status_codes=True,
    should_ignore_untemplated=True,
    should_respect_env_var=False,
    should_instrument_requests_inprogress=True,
    excluded_handlers=["/metrics"],
    inprogress_name="fastapi_inprogress",
    inprogress_labels=True,
)

# Добавляем метрики и внедряем их в FastAPI
instrumentator.instrument(app).expose(app)


@app.get(
    "/healthcheck",
    summary="Проверить работоспособность и доступность сервиса",
    tags=["Доступность"],
)
async def health_check_route() -> HealthcheckResponseSchema:
    """
    Возвращает информацию о сервисе.

    Доступно без аутентификации.
    """

    return HealthcheckResponseSchema(
        status="OK",
        title=settings.PROJECT_NAME,
        version=settings.APP_VERSION,
        message="See /docs for API documentation",
    )


@app.head(
    "/healthcheck",
    summary="Проверить работоспособность и доступность сервиса",
    status_code=status.HTTP_200_OK,
    tags=["Доступность"],
)
async def health_check_head() -> dict:
    """Для UptimeRobot."""
    return {
        "status": "OK",
    }


@app.get(
    "/",
    summary="Страница с информацией о сервисе и ссылками на документацию",
    response_class=HTMLResponse,
    tags=["Прочее"],
)
def home():
    """Выводит ссылки для перехода к документации сервиса."""

    return f"""
    <html>
        <head><title>{settings.PROJECT_NAME}</title></head>
        <body>
            <h1>{settings.PROJECT_NAME}</h1>
            <ul>
                <li><a href="/docs">Документация Swagger</a></li>
                <li><a href="/redoc">Документация ReDoc</a></li>
            </ul>
        </body>
    </html>
    """
