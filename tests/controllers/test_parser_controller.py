from unittest import mock

import pytest
from controllers.parser_controller import ParserController
from httpx import AsyncClient
from models.project import Project
from sqlmodel.ext.asyncio.session import AsyncSession


@pytest.fixture
def async_mock_client():
    return mock.AsyncMock(spec=AsyncClient)


@pytest.fixture
def async_mock_session():
    return mock.AsyncMock(spec=AsyncSession)


async def mock_response_func(url: str, *arg, **kwarg):
    mock_response = mock.AsyncMock()
    mock_response.url = url
    if url == "http://example.com":
        mock_response.text = """
        <html>
        Aggregate page
        <div><a href="/test" class="mock_class">Page link</a></html>
        </html>"""
    else:
        mock_response.text = """<html>
        <title>Article page</title>
        <div class="mock_image"><img src="/mock_img.png" /></div>
        <section class="mock_body_1">First body </section>
        <section class="mock_body_2">Second body</section>
        </html>"""
    return mock_response


@pytest.mark.asyncio
async def test_parser_controller(async_mock_session, async_mock_client):
    project = Project(
        id=1,
        name="Mock project",
        url="http://example.com",
        parse_type="html",
        parse_article_url_element={"selector": "a", "attrs": "mock_class"},
        parse_article_img_element={"selector": "div", "attrs": "mock_image"},
        parse_article_body_element={
            "selector": "section",
            "attrs": ["mock_body_1", "mock_body_2"],
        },
    )
    parser_controller = ParserController(async_mock_session)

    async_mock_session.get.return_value = project
    async_mock_session.exec.return_value = mock.MagicMock()

    async_mock_client.__aenter__.return_value.get = mock_response_func

    with mock.patch(
        "controllers.parser_controller.get_request_client",
        return_value=async_mock_client,
    ):
        result = await parser_controller.collect_data(project_id=1)

        async_mock_session.add.assert_called_once()
        async_mock_session.commit.assert_called_once()
        async_mock_session.refresh.assert_called_once()

        assert len(result) == 1
        assert result[0].project_id == 1
        assert result[0].url == "http://example.com/test"
