import requests
import json

class AuthClient:
    def __init__(self, base_url="http://localhost:8000/api"):
        """
        Initialize the authentication client with base URL
        
        :param base_url: Base URL of the FastAPI server
        """
        self.base_url = base_url
        self.access_token = None

    def register(self, username, email, password):
        """
        Register a new user
        
        :param username: Username for the new user
        :param email: Email for the new user
        :param password: Password for the new user
        :return: Response from the registration endpoint
        """
        url = f"{self.base_url}/register"
        payload = {
            "username": username,
            "email": email,
            "password": password
        }
        
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Registration error: {e}")
            return None

    def login(self, username, password):
        """
        Login and obtain an access token
        
        :param username: Username for login
        :param password: Password for login
        :return: Access token or None if login fails
        """
        url = f"{self.base_url}/token"
        payload = {
            "username": username,
            "password": password
        }
        
        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            return self.access_token
        except requests.exceptions.RequestException as e:
            print(f"Login error: {e}")
            return None

    def get_current_user(self):
        """
        Retrieve the current user's information
        
        :return: User information or None if request fails
        """
        if not self.access_token:
            print("No access token. Please login first.")
            return None
        
        url = f"{self.base_url}/users/me"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Get user error: {e}")
            return None

    def update_user(self, **update_data):
        """
        Update the current user's information
        
        :param update_data: Keyword arguments for user update (e.g., email, username)
        :return: Updated user information or None if request fails
        """
        if not self.access_token:
            print("No access token. Please login first.")
            return None
        
        url = f"{self.base_url}/users/me"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.put(url, json=update_data, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Update user error: {e}")
            return None

    def delete_user(self):
        """
        Delete the current user's account
        
        :return: Deleted user information or None if request fails
        """
        if not self.access_token:
            print("No access token. Please login first.")
            return None
        
        url = f"{self.base_url}/users/me"
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        
        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Delete user error: {e}")
            return None

def main():
    # Example usage of the AuthClient
    client = AuthClient()

    # Register a new user
    print("Registering new user...")
    registration = client.register("testuser", "test@example.com", "password123")
    if registration:
        print("Registration successful:", registration)

    # Login
    print("\nLogging in...")
    token = client.login("testuser", "password123")
    if token:
        print("Login successful. Token:", token)

        # Get current user info
        print("\nFetching user info...")
        user_info = client.get_current_user()
        if user_info:
            print("User Info:", json.dumps(user_info, indent=2))

        # Update user (example)
        print("\nUpdating user email...")
        updated_user = client.update_user(email="newemail@example.com")
        if updated_user:
            print("Updated User:", json.dumps(updated_user, indent=2))

        # Optional: Uncomment to test account deletion
        print("\nDeleting user account...")
        deleted_user = client.delete_user()
        if deleted_user:
            print("Deleted User:", json.dumps(deleted_user, indent=2))

if __name__ == "__main__":
    main()