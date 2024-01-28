from unittest.mock import AsyncMock, MagicMock

import pytest
from models.setting import Setting
from repositories.settings_repository import SettingsRepository
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture
def mock_async_session():
    session = AsyncMock(spec=AsyncSession)
    session.exec.return_value = MagicMock()
    return session


@pytest.fixture
def settings_repository(mock_async_session):
    return SettingsRepository(mock_async_session)


@pytest.mark.asyncio
async def test_retrieve_settings_by_project_id(
    settings_repository, mock_async_session
):
    project_id = 1
    test_settings = [
        Setting(id=1, project_id=project_id, name="Test Setting 1")
    ]
    session = mock_async_session.exec.return_value.unique
    session.return_value.all.return_value = test_settings

    result = await settings_repository.retrieve_settings_by_project_id(
        project_id
    )

    assert result == test_settings
    mock_async_session.exec.assert_awaited_once()


@pytest.mark.asyncio
async def test_retrieve_setting_by_project_id_and_network_name(
    settings_repository, mock_async_session
):
    project_id = 1
    network_name = "Test Network"
    test_setting = Setting(id=1, project_id=project_id, name=network_name)
    session = mock_async_session.exec.return_value.unique
    session.return_value.first.return_value = test_setting

    setting_repo = (
        settings_repository.retrieve_setting_by_project_id_and_network_name
    )
    result = await setting_repo(project_id, network_name)

    assert result == test_setting
    mock_async_session.exec.assert_awaited_once()


@pytest.mark.asyncio
async def test_retrieve_unique_settings(
    settings_repository, mock_async_session
):
    test_setting_names = ["Setting1", "Setting2"]
    session = mock_async_session.exec.return_value.unique
    session.return_value.all.return_value = test_setting_names

    result = await settings_repository.retrieve_unique_settings()

    assert result == test_setting_names
    mock_async_session.exec.assert_awaited_once()
