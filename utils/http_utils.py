import requests

def get_user_agent():
    try:
        url = "http://httpbin.org/user-agent"
        response = requests.get(url)
        response.raise_for_status()

        user_agent = response.json().get('user-agent')
        if not user_agent:
            raise ValueError("User agent not found in the response.")
        return user_agent

    except requests.RequestException as e:
        raise RuntimeError(f"Failed to retrieve user agent: {e}")
    except ValueError as e:
        raise RuntimeError(f"Data processing error: {e}")