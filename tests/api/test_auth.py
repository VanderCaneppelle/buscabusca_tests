import pytest
import requests
import json
from conftest import supabase_config, test_credentials, auth_headers


class TestSupabaseAuth:

    def test_login_success(self, supabase_config, test_credentials, auth_headers):
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
            headers=auth_headers
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

    def test_login_invalid_credentials(self, supabase_config, test_credentials, auth_headers):
        """Test login failure with invalid credentials"""
        url = f"{supabase_config['auth_url']}/token"
        payload = {
            "email": test_credentials['invalid_email'],
            "password": test_credentials['invalid_password']
        }

        response = requests.post(
            url,
            json=payload,
            params={"grant_type": "password"},
            headers=auth_headers
        )

        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

        assert response.status_code == 400
        data = response.json()
        assert "error" in data
        assert "Invalid login credentials" in data["error_description"]

    def test_login_missing_email(self, supabase_config, auth_headers):
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
            headers=auth_headers
        )

        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    def test_login_missing_password(self, supabase_config, test_credentials, auth_headers):
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
            headers=auth_headers
        )

        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    def test_signup_success(self, supabase_config, auth_headers):
        """Test successful user registration"""
        url = f"{supabase_config['auth_url']}/signup"
        payload = {
            "email": "newuser@example.com",
            "password": "password123"
        }

        response = requests.post(
            url,
            json=payload,
            headers=auth_headers
        )

        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

        assert response.status_code == 200
        data = response.json()
        assert "user" in data
        assert data["user"]["email"] == "newuser@example.com"

    def test_signup_duplicate_email(self, supabase_config, test_credentials, auth_headers):
        """Test signup failure with duplicate email"""
        url = f"{supabase_config['auth_url']}/signup"
        payload = {
            "email": test_credentials['valid_email'],
            "password": "password123"
        }

        response = requests.post(
            url,
            json=payload,
            headers=auth_headers
        )

        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")

        assert response.status_code == 400
        data = response.json()
        assert "error" in data

    def test_logout_success(self, supabase_config, test_credentials, auth_headers):
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
            headers=auth_headers
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

    def test_get_user_info(self, supabase_config, test_credentials, auth_headers):
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
            headers=auth_headers
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
