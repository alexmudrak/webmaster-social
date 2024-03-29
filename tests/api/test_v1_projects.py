import pytest


# TODO: Add ENDPOINT to global variable
# TODO: Add tests for check available keys
@pytest.mark.asyncio()
async def test_get_all_projects_v1(async_client):
    async with async_client as client:
        response = await client.get("/api/v1/projects/")

        assert response.status_code == 200
        assert len(response.json()) == 0


@pytest.mark.asyncio()
async def test_get_project_detail_v1(async_client, exist_project):
    exist_object = await exist_project
    async with async_client as client:
        response = await client.get(f"/api/v1/projects/{exist_object.id}")

        assert response.status_code == 200
        assert response.json()["name"] == exist_object.name
        assert response.json()["url"] == exist_object.url
        assert response.json()["active"] == exist_object.active


@pytest.mark.asyncio()
async def test_not_found_project_v1(async_client):
    async with async_client as client:
        response = await client.get("/api/v1/projects/1")

        assert response.status_code == 404


@pytest.mark.asyncio()
async def test_create_project_v1(async_client):
    payload = {
        "name": "new test",
        "url": "https://new-test.com/",
        "active": True,
    }
    async with async_client as client:
        response = await client.post("/api/v1/projects/", json=payload)

        assert response.status_code == 201
        assert response.json()["name"] == payload["name"]
        assert response.json()["url"] == payload["url"]
        assert response.json()["active"] == payload["active"]


@pytest.mark.asyncio()
async def test_create_duplicate_project_v1(async_client):
    payload = {
        "name": "new test",
        "url": "https://new-test.com/",
        "active": True,
    }
    async with async_client as client:
        await client.post("/api/v1/projects/", json=payload)
        response = await client.post("/api/v1/projects/", json=payload)

        assert response.status_code == 409


@pytest.mark.asyncio()
async def test_update_project_v1(async_client):
    payload = {
        "name": "new test",
        "url": "https://new-test.com/",
        "active": True,
    }
    new_payload = {
        "name": "updated test",
        "url": "https://updated-test.com/",
        "active": False,
    }
    async with async_client as client:
        new_project = await client.post("/api/v1/projects/", json=payload)
        response = await client.patch(
            f"/api/v1/projects/{new_project.json()['id']}", json=new_payload
        )

        assert response.status_code == 200


@pytest.mark.asyncio()
async def test_delete_project_v1(async_client):
    payload = {
        "name": "new test",
        "url": "https://new-test.com/",
        "active": True,
    }
    async with async_client as client:
        new_project = await client.post("/api/v1/projects/", json=payload)
        response = await client.delete(
            f"/api/v1/projects/{new_project.json()['id']}"
        )
        check_response = await client.get(
            f"/api/v1/projects/{new_project.json()['id']}"
        )

        assert response.status_code == 200
        assert check_response.status_code == 404
