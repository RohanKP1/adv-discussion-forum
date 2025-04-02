import requests
from typing import Dict, Any, Optional
from .auth import AuthClient

class RESTAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000/api", auth_client: Optional[AuthClient] = None):
        """
        Initialize REST API Client
        
        Args:
            base_url (str): Base URL for REST API
            auth_client (AuthClient, optional): Authentication client for headers
        """
        self.base_url = base_url
        self.auth_client = auth_client

    def _get_headers(self) -> Dict[str, str]:
        """
        Generate authentication headers
        
        Returns:
            Dict[str, str]: Headers with access token
        """
        return self.auth_client.get_headers() if self.auth_client else {}

    def register_user(self, username: str, email: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Register a new user
        
        Args:
            username (str): Username
            email (str): Email address
            password (str): Password
        
        Returns:
            Dict or None: Registered user details or None if error
        """
        try:
            response = requests.post(
                f"{self.base_url}/register", 
                json={
                    "username": username,
                    "email": email,
                    "password": password
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"User registration failed: {e}")
            return None

    def get_user_profile(self) -> Optional[Dict[str, Any]]:
        """
        Fetch current user's profile
        
        Returns:
            Dict or None: User profile details or None if error
        """
        try:
            response = requests.get(
                f"{self.base_url}/users/me",
                headers=self._get_headers()
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch user profile: {e}")
            return None

    def update_user_profile(self, updated_profile) -> Optional[Dict[str, Any]]:

        try:
            response = requests.put(
                f"{self.base_url}/users/me",
                headers=self._get_headers(),
                json=updated_profile
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to update user profile: {e}")
            return None
        
    
    def change_password(self, old_password: str, new_password: str) -> Optional[Dict[str, Any]]:
        """
        Change user password
        
        Args:
            old_password (str): Old password
            new_password (str): New password
        
        Returns:
            Dict or None: Result of password change or None if error
        """
        try:
            response = requests.put(
                f"{self.base_url}/users/me/password",
                headers=self._get_headers(),
                params={
                    "current_password": old_password,
                    "new_password": new_password
                }
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to change password: {e}")
            return None
