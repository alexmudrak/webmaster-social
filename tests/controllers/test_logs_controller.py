from unittest.mock import AsyncMock, patch

import pytest
from controllers.logs_controller import LogsController
from models.log_entry import LogEntry
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture
def mock_async_session():
    return AsyncMock(spec=AsyncSession)


@pytest.fixture
def logs_controller(mock_async_session):
    return LogsController(mock_async_session)


@pytest.mark.asyncio
async def test_get_all_objects(logs_controller):
    mock_log_entries = [
        LogEntry(
            id=1,
            message="Test log entry",
            logger_name="Mock logger",
            level="DEBUG",
        )
    ]
    with patch(
        "repositories.logs_repository.LogsRepository.retrieve_all_logs",
        return_value=mock_log_entries,
    ):
        result = await logs_controller.get_all_objects()

        assert result == mock_log_entries
