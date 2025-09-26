import pytest
import requests as r
from config import API_BASE_URL


@pytest.fixture(scope="session")
def base_url():
    return API_BASE_URL


@pytest.fixture(scope="session")
def session():
    with r.Session() as s:
        s.headers.update({"Content-Type": "application/json"})
        yield s
        s.close()


@pytest.fixture
def not_payment_payload():
    return {"type": "subscription",
            "data": {
                "id": "123"
            }}


@pytest.fixture
def payment_correct_payload():
    return {"type": "payment",
            "data": {
                "id": "123456"
            }}
