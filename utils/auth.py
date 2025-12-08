import requests
from config import API_BASE_URL

def register_user(username, email, password):
    """
    Registers a new user with the given username, email, and password.

    Args:
        username (str): The username of the user to register.
        email (str): The email of the user to register.
        password (str): The password of the user to register.

    Returns:
        tuple: A tuple containing the response JSON and the status code of the request.
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/register",
            json={"username": username, "email": email, "password": password}
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def login_user(username, password):
    """
    Logs in a user with the given username and password.

    Args:
        username (str): The username of the user to log in.
        password (str): The password of the user to log in.

    Returns:
        tuple: A tuple containing the response JSON and the status code of the request.
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/auth/login",
            json={"username": username, "password": password}
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def get_current_user(token):
    """
    Retrieves the user associated with the given token.

    Args:
        token (str): The token of the user to retrieve.

    Returns:
        tuple: A tuple containing the response JSON and the status code of the request.
    """
    try:
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.get(f"{API_BASE_URL}/auth/me", headers=headers)
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500