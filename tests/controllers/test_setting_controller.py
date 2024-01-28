from unittest.mock import AsyncMock, MagicMock

import pytest
from controllers.setting_controller import SettingController
from fastapi import HTTPException
from models.setting import Setting
from schemas.setting_schema import SettingCreate, SettingRead
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture
def mock_async_session():
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.fixture
def setting_controller(mock_async_session):
    return SettingController(mock_async_session)


@pytest.mark.asyncio
async def test_get_all_objects(
    setting_controller,
    mock_async_session,
):
    mock_setting = MagicMock(spec=Setting)
    mock_setting.model_dump.return_value = {
        "id": 1,
        "name": "Test Setting",
        "settings": {},
        "project_id": 1,
        "active": True,
    }
    mock_setting.project = None
    mock_exec = MagicMock()
    mock_exec.unique.return_value.all.return_value = [mock_setting]
    mock_async_session.exec.return_value = mock_exec

    result = await setting_controller.get_all_objects()

    assert len(result) == 1
    assert isinstance(result[0], SettingRead)
    assert result[0].id == 1
    mock_async_session.exec.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_object_success(
    setting_controller,
    mock_async_session,
):
    test_data = SettingCreate(
        name="Test", settings={}, project_id=1, active=True
    )
    mock_exec = MagicMock()
    mock_exec.unique.return_value.one_or_none.return_value = None
    mock_async_session.exec.return_value = mock_exec

    created_object = await setting_controller.create_object(test_data)

    assert created_object.name == test_data.name
    mock_async_session.add.assert_called_once()
    mock_async_session.commit.assert_awaited_once()
    mock_async_session.refresh.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_object_existing(
    setting_controller,
    mock_async_session,
):
    test_data = SettingCreate(
        name="Test", settings={}, project_id=1, active=True
    )
    existing_setting = Setting(
        name="Test", settings={}, project_id=1, active=True
    )
    mock_exec = MagicMock()
    mock_exec.unique.return_value.one_or_none.return_value = existing_setting
    mock_async_session.exec.return_value = mock_exec

    with pytest.raises(HTTPException) as exc_info:
        await setting_controller.create_object(test_data)

    assert exc_info.value.status_code == 409
    mock_async_session.add.assert_not_called()
    mock_async_session.commit.assert_not_called()
