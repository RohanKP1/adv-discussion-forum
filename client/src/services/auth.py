import requests
from typing import Optional, Dict, Any

class AuthClient:
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        """
        Initialize AuthClient with base URL for authentication
        
        Args:
            base_url (str): Base URL for the authentication endpoint
        """
        self.base_url = base_url
        self.token: Optional[str] = None
        self.user_data: Optional[Dict[str, Any]] = None

    def login(self, username: str, password: str) -> bool:
        """
        Authenticate user and store access token
        
        Args:
            username (str): User's username
            password (str): User's password
        
        Returns:
            bool: True if login successful, False otherwise
        """
        try:
            response = requests.post(
                f"{self.base_url}/token", 
                data={
                    "username": username, 
                    "password": password,
                    "grant_type": "password"
                }
            )
            response.raise_for_status()
            token_data = response.json()
            self.token = token_data['access_token']
            
            # Fetch user details
            self.fetch_user_details()
            
            return True
        except requests.exceptions.RequestException as e:
            print(f"Login failed: {e}")
            return False

    def fetch_user_details(self):
        """
        Fetch current user details after successful login
        """
        try:
            response = requests.get(
                f"{self.base_url}/users/me",
                headers=self.get_headers()
            )
            response.raise_for_status()
            self.user_data = response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to fetch user details: {e}")
            self.user_data = None

    def get_headers(self) -> Dict[str, str]:
        """
        Generate authentication headers
        
        Returns:
            Dict[str, str]: Headers with access token
        """
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def logout(self):
        """
        Clear authentication token and user data
        """
        self.token = None
        self.user_data = None

    def is_authenticated(self) -> bool:
        """
        Check if user is currently authenticated
        
        Returns:
            bool: True if authenticated, False otherwise
        """
        return self.token is not None