from app.core.config import settings


async def test_health_check_route_get(client):
    response = await client.get("/healthcheck")
    json = response.json()

    assert response.status_code == 200
    assert json["title"] == settings.PROJECT_NAME
    assert json["version"] == settings.APP_VERSION
    assert json["status"] == "OK"


async def test_health_check_route_head(client):
    response = await client.head("/healthcheck")

    assert response.status_code == 200
