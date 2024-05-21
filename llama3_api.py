import requests
import json

def get_response(prompt):
    api_url = "http://localhost:11434/api/chat"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}  # Replace with your actual API key
    payload = {
        "model": "llama3",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
        return data['message']['content']
    except requests.exceptions.HTTPError as http_err:
        return f"HTTP error occurred: {http_err}"
    except requests.exceptions.ConnectionError as conn_err:
        return f"Connection error occurred: {conn_err}"
    except requests.exceptions.Timeout as timeout_err:
        return f"Timeout error occurred: {timeout_err}"
    except requests.exceptions.RequestException as req_err:
        return f"An error occurred: {req_err}"

def get_response_stream(prompt):
    api_url = "http://localhost:11434/api/chat"
    headers = {"Authorization": "Bearer YOUR_API_KEY"}  # Replace with your actual API key
    payload = {
        "model": "llama3",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }

    try:
        response = requests.post(api_url, json=payload, headers=headers, stream=True)
        response.raise_for_status()

        for chunk in response.iter_lines():
            if chunk:
                data = json.loads(chunk.decode('utf-8'))
                if 'message' in data:
                    yield data['message']['content']
    except requests.exceptions.HTTPError as http_err:
        yield f"HTTP error occurred: {http_err}"
    except requests.exceptions.ConnectionError as conn_err:
        yield f"Connection error occurred: {conn_err}"
    except requests.exceptions.Timeout as timeout_err:
        yield f"Timeout error occurred: {timeout_err}"
    except requests.exceptions.RequestException as req_err:
        yield f"An error occurred: {req_err}"

