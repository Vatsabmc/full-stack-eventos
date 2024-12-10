import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.event import create_random_event
from app.tests.utils.status import create_random_status
from app.tests.utils.category import create_random_category
from app.tests.utils.user import create_random_user


def test_create_event(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    organizer = create_random_user()
    status = create_random_status()
    category = create_random_category()
    data = {
        "title": "Event1",
        "description": "dummy event",
        "start_datetime": "2027-12-05T10:07:15.15-05:00",
        "end_datetime": "2027-12-05T19:07:15.157Z",
        "location": "string",
        "capacity": 6,
        "organizer_id": organizer.id,
        "status_id": status.id,
        "category_id": category.id
        }
    response = client.post(
        f"{settings.API_V1_STR}/events/",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert "id" in content
    assert "organizer_id" in content


def test_read_event(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    event = create_random_event(db)
    response = client.get(
        f"{settings.API_V1_STR}/events/{event.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == event.title
    assert content["description"] == event.description
    assert content["id"] == str(event.id)
    assert content["organizer_id"] == str(event.organizer_id)


def test_read_event_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/events/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Event not found"


def test_read_event_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    event = create_random_event(db)
    response = client.get(
        f"{settings.API_V1_STR}/events/{event.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_events(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    create_random_event(db)
    create_random_event(db)
    response = client.get(
        f"{settings.API_V1_STR}/events/",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_update_event(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    event = create_random_event(db)
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/events/{event.id}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["title"] == data["title"]
    assert content["description"] == data["description"]
    assert content["id"] == str(event.id)
    assert content["organizer_id"] == str(event.organizer_id)


def test_update_event_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/events/{uuid.uuid4()}",
        headers=superuser_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Event not found"


def test_update_event_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    event = create_random_event(db)
    data = {"title": "Updated title", "description": "Updated description"}
    response = client.put(
        f"{settings.API_V1_STR}/events/{event.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_delete_event(
    client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    event = create_random_event(db)
    response = client.delete(
        f"{settings.API_V1_STR}/events/{event.id}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Event deleted successfully"


def test_delete_event_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/events/{uuid.uuid4()}",
        headers=superuser_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Event not found"


def test_delete_event_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    event = create_random_event(db)
    response = client.delete(
        f"{settings.API_V1_STR}/events/{event.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Not enough permissions"
