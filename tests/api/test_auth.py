import os
import uuid
import pytest
import requests
import json
from conftest import supabase_config, test_credentials, auth_headers_service_key, auth_headers_anon_key, supabase_admin


class TestSupabaseAuth:

    def test_login_success(self, supabase_config, test_credentials, auth_headers_anon_key):
        """Test successful login with valid credentials"""
        url = f"{supabase_config['auth_url']}/token"
        payload = {
            "email": test_credentials['valid_email'],
            "password": test_credentials['valid_password']
        }

        response = requests.post(
            url,
            json=payload,
            params={"grant_type": "password"},
            headers=auth_headers_anon_key
        )

        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "expires_in" in data
        assert "expires_at" in data
        # Removido: assert "session" in data (não existe na resposta)

    def test_login_invalid_credentials(self, supabase_config, test_credentials, auth_headers_anon_key):
        """Test login failure with invalid credentials"""
        url = f"{supabase_config['auth_url']}/token"
        payload = {
            "email": test_credentials['invalid_email'],
            "password": test_credentials['invalid_password'],
            "full_name": "Vander Caneppelle",
            "phone": "11999999999"

        }

        response = requests.post(
            url,
            json=payload,
            params={"grant_type": "password"},
            headers=auth_headers_anon_key
        )

        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

        assert response.status_code == 400
        data = response.json()
        assert "error_code" in data
        assert "Invalid login credentials" in data["msg"]

    def test_login_missing_email(self, supabase_config, auth_headers_anon_key):
        """Test login failure with missing email"""
        url = f"{supabase_config['auth_url']}/token"
        payload = {
            "email": "",
            "password": "password123"
        }

        response = requests.post(
            url,
            json=payload,
            params={"grant_type": "password"},
            headers=auth_headers_anon_key
        )

        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

        assert response.status_code == 400
        data = response.json()
        assert "error_code" in data
        assert "missing email or phone" in data["msg"]

    def test_login_missing_password(self, supabase_config, test_credentials, auth_headers_anon_key):
        """Test login failure with missing password"""
        url = f"{supabase_config['auth_url']}/token"
        payload = {
            "email": test_credentials['valid_email'],
            "password": ""
        }

        response = requests.post(
            url,
            json=payload,
            params={"grant_type": "password"},
            headers=auth_headers_anon_key
        )

        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

        assert response.status_code == 400
        data = response.json()
        assert "error_code" in data
        assert "Invalid login credentials" in data["msg"]

    def test_logout_success(self, supabase_config, test_credentials, auth_headers_anon_key):
        """Test successful logout"""
        # First login to get token
        login_url = f"{supabase_config['auth_url']}/token"
        login_payload = {
            "email": test_credentials['valid_email'],
            "password": test_credentials['valid_password']
        }

        login_response = requests.post(
            login_url,
            json=login_payload,
            params={"grant_type": "password"},
            headers=auth_headers_anon_key
        )

        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]

        # Then logout
        logout_url = f"{supabase_config['auth_url']}/logout"
        logout_headers = {
            "Authorization": f"Bearer {access_token}",
            "apikey": supabase_config['anon_key'],
            "Content-Type": "application/json"
        }

        logout_response = requests.post(logout_url, headers=logout_headers)

        assert logout_response.status_code == 204

    def test_get_user_info(self, supabase_config, test_credentials, auth_headers_anon_key):
        """Test getting user information with valid token"""
        # First login to get token
        login_url = f"{supabase_config['auth_url']}/token"
        login_payload = {
            "email": test_credentials['valid_email'],
            "password": test_credentials['valid_password']
        }

        login_response = requests.post(
            login_url,
            json=login_payload,
            params={"grant_type": "password"},
            headers=auth_headers_anon_key
        )

        assert login_response.status_code == 200
        access_token = login_response.json()["access_token"]

        # Get user info
        user_url = f"{supabase_config['auth_url']}/user"
        user_headers = {
            "Authorization": f"Bearer {access_token}",
            "apikey": supabase_config['anon_key'],
            "Content-Type": "application/json"
        }

        user_response = requests.get(user_url, headers=user_headers)

        assert user_response.status_code == 200
        data = user_response.json()
        assert "id" in data
        assert "email" in data
        assert data["email"] == test_credentials['valid_email']

    def test_user_creation(self, temp_user):
        assert temp_user["id"] is not None

    def test_new_signup(self, supabase_config, auth_headers_anon_key, test_credentials, supabase_admin):

        email = f"u_{uuid.uuid4().hex[:8]}@gmail.com"

        signup_url = f"{supabase_config['signup_url']}"

        signup_payload = {
            "email": email,
            "password": test_credentials['valid_password'],

        }

        r = requests.post(signup_url, json=signup_payload,
                          headers=auth_headers_anon_key)

        assert r.status_code == 200
        data = r.json()
        print(data)
        assert data["success"] is True

        user_id = data["userId"]

        if user_id:
            supabase_admin.auth.admin.delete_user(user_id)

    def test_user_duplicated(self, supabase_config, auth_headers_anon_key, test_credentials):

        signup_url = f"{supabase_config['signup_url']}"

        signup_payload = {
            "email": supabase_config['confirmed_user_email'],
            "password": test_credentials['valid_password']
        }

        r = requests.post(signup_url, json=signup_payload,
                          headers=auth_headers_anon_key)
        print(r)

        assert r.status_code == 409
        data = r.json()
        print(data)
        assert data["code"] in ("EMAIL_TAKEN", "EMAIL_PENDING")
        assert data["message"] == "E-mail já cadastrado"
