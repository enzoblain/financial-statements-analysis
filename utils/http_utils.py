import requests

def get_user_agent():
    """
    Retrieves the current user agent string used by the client making the request.

    This function sends a GET request to the httpbin.org service, which returns the user agent
    string that the client used to make the request. The user agent string is then extracted
    from the JSON response and returned.

    Returns:
        str: The user agent string.

    Raises:
        requests.RequestException: If the HTTP request fails or the response cannot be parsed.
    """
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

