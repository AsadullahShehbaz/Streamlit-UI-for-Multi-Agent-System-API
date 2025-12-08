import requests
from config import API_BASE_URL

def get_headers(token):
    if token:
        return {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    return {"Content-Type": "application/json"}

def create_research(token, query, max_iterations=2):
    try:
        response = requests.post(
            f"{API_BASE_URL}/research/",
            headers=get_headers(token),
            json={"query": query, "max_iterations": max_iterations}
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def get_research_history(token, skip=0, limit=10):
    try:
        response = requests.get(
            f"{API_BASE_URL}/research/history?skip={skip}&limit={limit}",
            headers=get_headers(token)
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def get_research_by_id(token, research_id):
    try:
        response = requests.get(
            f"{API_BASE_URL}/research/{research_id}",
            headers=get_headers(token)
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def delete_research(token, research_id):
    try:
        response = requests.delete(
            f"{API_BASE_URL}/research/{research_id}",
            headers=get_headers(token)
        )
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500

def health_check():
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        return response.json(), response.status_code
    except Exception as e:
        return {"error": str(e)}, 500