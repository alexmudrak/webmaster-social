from unittest.mock import AsyncMock, MagicMock

import pytest
from models.log_entry import LogEntry
from repositories.logs_repository import LogsRepository
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture
def mock_async_session():
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.fixture
def logs_repository(mock_async_session):
    return LogsRepository(mock_async_session)


@pytest.mark.asyncio
async def test_retrieve_all_logs(logs_repository, mock_async_session):
    # Arrange
    test_logs = [
        LogEntry(
            id=1,
            message="Test Log 1",
            level="DEBUG",
            logger_name="Mock logger 1",
        ),
        LogEntry(
            id=2,
            message="Test Log 2",
            level="INFO",
            logger_name="Mock logger 2",
        ),
    ]

    mock_exec = MagicMock()
    mock_exec.unique.return_value.all.return_value = test_logs
    mock_async_session.exec.return_value = mock_exec

    # Act
    result = await logs_repository.retrieve_all_logs()

    # Assert
    assert result == test_logs
    mock_async_session.exec.assert_awaited_once()
