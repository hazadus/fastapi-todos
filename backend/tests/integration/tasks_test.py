import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.tasks import router as tasks_router
from app.models import TaskModel, UserModel
from app.schemas import TaskCreateSchema, TaskUpdateSchema
from app.services import create_task, create_user_token
from tests.integration.conftest import BaseTestRouter


@pytest.fixture()
def task_data() -> TaskCreateSchema:
    """Фикстура для создания данных задачи."""
    return TaskCreateSchema(
        title="Тестовая задача",
        description="Это тестовая задача.",
    )


@pytest_asyncio.fixture(scope="function")
async def task(
    session: AsyncSession,
    user: UserModel,
    task_data: TaskCreateSchema,
) -> TaskModel:
    """Фикстура для создания задачи в БД."""
    return await create_task(
        session=session,
        task_data=task_data,
        user_id=user.id,
    )


@pytest.fixture()
def user_token(user: UserModel) -> str:
    """Фикстура для создания токена пользователя."""
    return create_user_token(user=user)


class TestTasksRouter(BaseTestRouter):
    router = tasks_router

    # MARK: List
    async def test_tasks_list_without_token(
        self,
        client: AsyncClient,
    ):
        """Тестирует получение списка задач без токена."""
        response = await client.get("/tasks")
        assert response.status_code == 403

    async def test_tasks_list_with_token(
        self,
        client: AsyncClient,
        user_token: str,
        task: TaskModel,
    ):
        """Тестирует успешное получение списка задач с токеном."""
        response = await client.get(
            "/tasks",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        json = response.json()

        assert response.status_code == 200
        # В списке должна быть одна задача, созданная в фикстуре task
        assert len(json["tasks"]) == 1

    # MARK: Create
    async def test_task_create_without_token(
        self,
        client: AsyncClient,
        task_data: TaskCreateSchema,
    ):
        """Тестирует создание задачи без токена."""
        response = await client.post(
            "/tasks",
            json=task_data.model_dump(),
        )
        assert response.status_code == 403

    async def test_task_create_with_token(
        self,
        client: AsyncClient,
        user_token: str,
        task_data: TaskCreateSchema,
    ):
        """Тестирует успешное создание задачи с токеном."""
        response = await client.post(
            "/tasks",
            json=task_data.model_dump(),
            headers={"Authorization": f"Bearer {user_token}"},
        )
        json = response.json()

        assert response.status_code == 201
        assert json["title"] == task_data.title
        assert json["description"] == task_data.description

    # MARK: Update
    async def test_update_task_without_token(
        self,
        client: AsyncClient,
        task: TaskModel,
    ):
        """Тестирует обновление задачи без токена."""
        response = await client.patch(
            f"/tasks/{task.id}",
            json=TaskUpdateSchema(title="Измененный заголовок").model_dump(),
        )
        assert response.status_code == 403

    async def test_update_task_with_token(
        self,
        client: AsyncClient,
        user_token: str,
        task: TaskModel,
    ):
        """Тестирует успешное обновление задачи с токеном."""
        updated_title = "Измененный заголовок"
        updated_description = "Обновленное описание задачи"
        response = await client.patch(
            f"/tasks/{task.id}",
            json=TaskUpdateSchema(
                title=updated_title,
                description=updated_description,
            ).model_dump(),
            headers={"Authorization": f"Bearer {user_token}"},
        )
        json = response.json()

        assert response.status_code == 200
        assert json["title"] == updated_title
        assert json["description"] == updated_description

    # MARK: Delete
    async def test_delete_task_without_token(
        self,
        client: AsyncClient,
        task: TaskModel,
    ):
        """Тестирует удаление задачи без токена."""
        response = await client.delete(f"/tasks/{task.id}")
        assert response.status_code == 403

    async def test_delete_task_with_token(
        self,
        client: AsyncClient,
        user_token: str,
        task: TaskModel,
    ):
        """Тестирует успешное удаление задачи с токеном."""
        response = await client.delete(
            f"/tasks/{task.id}",
            headers={"Authorization": f"Bearer {user_token}"},
        )

        assert response.status_code == 204

        # Проверяем, что задача действительно удалена
        response = await client.get(
            f"/tasks",
            headers={"Authorization": f"Bearer {user_token}"},
        )
        json = response.json()

        assert len(json["tasks"]) == 0
        assert json["total"] == 0
