import uuid
import pytest
import requests as r
from config import API_BASE_URL
from supabase import create_client, Client
import os

from dotenv import load_dotenv
load_dotenv()


@pytest.fixture(scope="session")
def supabase_config():
    url = os.getenv("SUPABASE_URL")
    service_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    anon_key = os.getenv("SUPABASE_ANON_KEY")

    # Variáveis hardcoded (não sensíveis)
    auth_url = "http://buscabusca.vercel.app/api/auth"
    confirmed_user_email = "vandercaneppelle@outlook.com"
    signup_url = "http://buscabusca.vercel.app/api/auth/signup"

    # assert url and service_key and anon_key, "Defina variaveis do SUPABASE"

    return {"url": url, "service_key": service_key, "anon_key": anon_key, "auth_url": auth_url, "confirmed_user_email": confirmed_user_email, "signup_url": signup_url}


@pytest.fixture(scope="session")
def supabase_admin(supabase_config) -> Client:
    return create_client(supabase_config["url"], supabase_config["service_key"])


@pytest.fixture(scope="session")
def supabase_anon(supabase_config) -> Client:
    return create_client(supabase_config["url"], supabase_config["anon_key"])


@pytest.fixture
def auth_headers_service_key(supabase_config):
    return {
        'apikey': supabase_config['service_key'],
        'Content-Type': 'application/json'
    }


@pytest.fixture
def auth_headers_anon_key(supabase_config):
    return {
        'apikey': supabase_config['anon_key'],
        'Content-Type': 'application/json'
    }


@pytest.fixture(scope="session")
def base_url():
    return API_BASE_URL


@pytest.fixture()
def temp_user(supabase_admin):
    email = f"test_{uuid.uuid4().hex[8:]}@example.com"
    password = "pass123"

    created = supabase_admin.auth.admin.create_user({
        "email": email,
        "password": password,
        "confirm_email": True,
    })

    # Extrai o id do usuário criado
    user_id = created.user.id if created.user else None

    yield {"id": user_id, "email": email, "password": password}

    # Cleanup - deleta o usuário depois do teste
    if user_id:
        supabase_admin.auth.admin.delete_user(user_id)


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
def test_credentials():
    return {
        'valid_email': 'vandercaneppelle@outlook.com',
        'valid_password': '123456',
        'invalid_email': 'emailinvalido@gmail.com',
        'invalid_password': 'wrongpassword'
    }
