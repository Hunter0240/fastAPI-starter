import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_item(client: AsyncClient, auth_headers: dict):
    resp = await client.post(
        "/items/",
        json={"title": "Test Item", "description": "A test"},
        headers=auth_headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["title"] == "Test Item"
    assert data["description"] == "A test"
    assert "id" in data


@pytest.mark.asyncio
async def test_create_item_no_auth(client: AsyncClient):
    resp = await client.post("/items/", json={"title": "No auth"})
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_list_items(client: AsyncClient, auth_headers: dict):
    await client.post("/items/", json={"title": "Item 1"}, headers=auth_headers)
    await client.post("/items/", json={"title": "Item 2"}, headers=auth_headers)
    resp = await client.get("/items/", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] >= 2
    assert len(data["items"]) >= 2


@pytest.mark.asyncio
async def test_get_item(client: AsyncClient, auth_headers: dict):
    create = await client.post(
        "/items/", json={"title": "Get Me"}, headers=auth_headers
    )
    item_id = create.json()["id"]
    resp = await client.get(f"/items/{item_id}", headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["title"] == "Get Me"


@pytest.mark.asyncio
async def test_get_item_not_found(client: AsyncClient, auth_headers: dict):
    resp = await client.get("/items/nonexistent", headers=auth_headers)
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_update_item(client: AsyncClient, auth_headers: dict):
    create = await client.post(
        "/items/", json={"title": "Old Title"}, headers=auth_headers
    )
    item_id = create.json()["id"]
    resp = await client.put(
        f"/items/{item_id}",
        json={"title": "New Title"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["title"] == "New Title"


@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient, auth_headers: dict):
    create = await client.post(
        "/items/", json={"title": "Delete Me"}, headers=auth_headers
    )
    item_id = create.json()["id"]
    resp = await client.delete(f"/items/{item_id}", headers=auth_headers)
    assert resp.status_code == 204
    get_resp = await client.get(f"/items/{item_id}", headers=auth_headers)
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_pagination(client: AsyncClient, auth_headers: dict):
    for i in range(5):
        await client.post(
            "/items/", json={"title": f"Page Item {i}"}, headers=auth_headers
        )
    resp = await client.get("/items/?offset=0&limit=2", headers=auth_headers)
    data = resp.json()
    assert len(data["items"]) == 2
    assert data["total"] >= 5
    assert data["offset"] == 0
    assert data["limit"] == 2
