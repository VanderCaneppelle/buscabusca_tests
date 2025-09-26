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


@pytest.fixture
def supabase_config():
    return {
        'url': 'https://rxozhlxmfbioqgqomkrz.supabase.co',
        'anon_key': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ4b3pobHhtZmJpb3FncW9ta3J6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTM5OTg0MDIsImV4cCI6MjA2OTU3NDQwMn0.MsMaFjnQYvDP7xSmHS-QY2P7jZ4JCnnxDmCo6y0lk4g',
        'auth_url': 'https://rxozhlxmfbioqgqomkrz.supabase.co/auth/v1'
    }


@pytest.fixture
def test_credentials():
    return {
        'valid_email': 'vandercaneppelle@outlook.com',
        'valid_password': '123456',
        'invalid_email': 'emailinvalido@gmail.com',
        'invalid_password': 'wrongpassword'
    }


@pytest.fixture
def auth_headers(supabase_config):
    return {
        'apikey': supabase_config['anon_key'],
        'Content-Type': 'application/json'
    }
