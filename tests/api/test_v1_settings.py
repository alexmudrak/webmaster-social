import pytest

ENDPOINT = "/api/v1/settings/"


@pytest.mark.asyncio()
async def test_get_all_settings_v1(async_client):
    async with async_client as client:
        response = await client.get(ENDPOINT)

        assert response.status_code == 200
        assert len(response.json()) == 0


@pytest.mark.asyncio()
async def test_get_setting_detail_with_project_v1(
    async_client, exist_setting_with_project
):
    exist_object = await exist_setting_with_project

    async with async_client as client:
        response = await client.get(ENDPOINT + str(exist_object.id))

        assert response.status_code == 200
        assert response.json()["name"] == exist_object.name
        assert response.json()["settings"] == exist_object.settings
        assert response.json()["active"] == exist_object.active
        assert response.json()["project"]["url"] == exist_object.project.url


@pytest.mark.asyncio()
async def test_get_setting_detail_without_project_v1(
    async_client, exist_setting_without_project
):
    exist_object = await exist_setting_without_project

    async with async_client as client:
        response = await client.get(ENDPOINT + str(exist_object.id))

        assert response.status_code == 200
        assert response.json()["project"] is None


@pytest.mark.asyncio()
async def test_not_found_setting_v1(async_client):
    async with async_client as client:
        response = await client.get(ENDPOINT + "1")

        assert response.status_code == 404
        assert response.json()["detail"] == "Setting not found"


@pytest.mark.asyncio()
async def test_create_setting_with_project_v1(async_client, exist_project):
    exist_project = await exist_project

    payload = {
        "name": "new test",
        "project_id": exist_project.id,
        "settings": {},
        "active": True,
    }
    async with async_client as client:
        response = await client.post(ENDPOINT, json=payload)

        assert response.status_code == 201
        assert response.json()["name"] == payload["name"]
        assert response.json()["settings"] == payload["settings"]
        assert response.json()["active"] == payload["active"]
        assert response.json()["project_id"] == exist_project.id
        assert response.json().get("project") is None


@pytest.mark.asyncio()
async def test_create_setting_without_project_v1(async_client):
    payload = {
        "name": "new test",
        "settings": {},
        "active": True,
    }
    async with async_client as client:
        response = await client.post(ENDPOINT, json=payload)

        assert response.status_code == 201
        assert response.json()["project_id"] is None


@pytest.mark.asyncio()
async def test_create_duplicate_setting_with_project_v1(
    async_client, exist_project
):
    exist_project = await exist_project

    payload = {
        "name": "new test",
        "settings": {},
        "project_id": exist_project.id,
        "active": True,
    }
    async with async_client as client:
        await client.post(ENDPOINT, json=payload)
        response = await client.post(ENDPOINT, json=payload)

        assert response.status_code == 409
        assert response.json()["detail"] == (
            "A object with the same name and project ID "
            "combination already exists."
        )


@pytest.mark.asyncio()
async def test_create_duplicate_setting_without_project_v1(async_client):
    payload = {
        "name": "new test",
        "settings": {},
        "active": True,
    }
    async with async_client as client:
        await client.post(ENDPOINT, json=payload)
        response = await client.post(ENDPOINT, json=payload)

        assert response.status_code == 409


@pytest.mark.asyncio()
async def test_update_setting_v1(async_client, exist_setting_with_project):
    exist_setting_with_project = await exist_setting_with_project

    new_payload = {
        "name": "updated test",
        "active": False,
    }
    async with async_client as client:
        response = await client.patch(
            ENDPOINT + str(exist_setting_with_project.id), json=new_payload
        )

        assert response.status_code == 200
        assert response.json()["name"] == new_payload["name"]
        assert response.json()["active"] is False
        assert response.json()["settings"] is None
        assert response.json()["project_id"] is None


@pytest.mark.asyncio()
async def test_delete_setting_v1(async_client, exist_setting_with_project):
    exist_setting_with_project = await exist_setting_with_project

    async with async_client as client:
        response = await client.delete(
            ENDPOINT + str(exist_setting_with_project.id)
        )
        check_response = await client.get(
            ENDPOINT + str(exist_setting_with_project.id)
        )

        assert response.status_code == 200
        assert check_response.status_code == 404
