from unittest.mock import AsyncMock, MagicMock

import pytest
from controllers.project_controller import ProjectController
from fastapi import HTTPException
from models.project import Project
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture
def mock_async_session():
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.fixture
def project_controller(mock_async_session):
    return ProjectController(mock_async_session)


@pytest.fixture
def project():
    project = MagicMock(spec=Project)
    project.id = 1
    project.name = "Mock project"
    project.url = "http://testproject.com"
    project.parse_article_body_element = "body"
    project.parse_article_img_element = "img"
    project.parse_article_url_element = "a"
    project.active = True

    return project


@pytest.mark.asyncio
async def test_get_all_objects(
    project_controller,
    mock_async_session,
    project,
):
    mock_exec = MagicMock()
    mock_exec.unique.return_value.all.return_value = [
        project,
        project,
    ]
    project_controller.session.exec.return_value = mock_exec

    result = await project_controller.get_all_objects()

    assert len(result) == 2
    mock_async_session.exec.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_object_found(
    project_controller,
    mock_async_session,
    project,
):
    project_controller.session.get.return_value = project

    result = await project_controller.get_object(1)

    assert result.id == 1
    mock_async_session.get.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_object_not_found(project_controller):
    project_controller.session.get.return_value = None
    with pytest.raises(HTTPException) as exc_info:
        await project_controller.get_object(999)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_create_object_without_url_raises_http_exception(
    project_controller,
    project,
):
    project.url = None

    with pytest.raises(HTTPException) as exc_info:
        await project_controller.create_object(project)

    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_create_object_with_existing_project_raises_http_exception(
    project_controller,
    project,
):
    mock_exec = MagicMock()
    mock_exec.unique.return_value.one_or_none.return_value = project
    project_controller.session.exec.return_value = mock_exec

    with pytest.raises(HTTPException) as exc_info:
        await project_controller.create_object(project)

    assert exc_info.value.status_code == 409


@pytest.mark.asyncio
async def test_create_object_successfully_creates_project(
    project_controller,
    mock_async_session,
    project,
):
    mock_exec = MagicMock()
    mock_exec.unique.return_value.one_or_none.return_value = None
    project_controller.session.exec.return_value = mock_exec

    new_project = await project_controller.create_object(project)

    assert new_project.name == project.name
    assert new_project.url == str(project.url)
    mock_async_session.add.assert_called_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_awaited_once_with(new_project)


@pytest.mark.asyncio
async def test_update_object_without_url_raises_http_exception(
    project_controller,
    project,
):
    project.url = None

    with pytest.raises(HTTPException) as exc_info:
        await project_controller.update_object(1, project)

    assert exc_info.value.status_code == 400


@pytest.mark.asyncio
async def test_update_object_with_nonexistent_project_raises_http_exception(
    project_controller,
    mock_async_session,
    project,
):
    mock_async_session.get.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await project_controller.update_object(1, project)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_update_object_successfully_updates_project(
    project_controller,
    mock_async_session,
    project,
):
    mock_async_session.get.return_value = project

    updated_project = await project_controller.update_object(1, project)

    assert updated_project.name == project.name
    assert updated_project.url == str(project.url)
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_awaited_once_with(project)


@pytest.mark.asyncio
async def test_delete_object_with_nonexistent_project_raises_http_exception(
    project_controller,
    mock_async_session,
):
    mock_async_session.get.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        await project_controller.delete_object(1)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_delete_object_successfully_deletes_project(
    project_controller,
    mock_async_session,
    project,
):
    mock_async_session.get.return_value = project

    response = await project_controller.delete_object(1)

    assert response == {"message": "Project `1` was deleted"}
    mock_async_session.delete.assert_called_once_with(project)
    mock_async_session.commit.assert_awaited_once()
