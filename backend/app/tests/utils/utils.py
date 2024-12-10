import random
import string
import faker
import datetime as datetime

from fastapi.testclient import TestClient

from app.core.config import settings

fake = Faker()


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def random_dates() -> datetime:

    start_datetime = fake.date_time_between(start_date='now', end_date='+1y')
    end_datetime = fake.date_time_between(start_date=start_datetime, end_date='+1y')
    return start_datetime, end_datetime


def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers
