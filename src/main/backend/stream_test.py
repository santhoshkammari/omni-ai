import requests
import json

def stream_chat(query, api_url="http://localhost:8888/api/chat", web_search=False):
    """
    Send a query to the chatbot API and yield the streamed response.

    Args:
    query (str): The user's input query.
    api_url (str): The URL of the chatbot API endpoint.
    web_search (bool): Whether to enable web search for the query.

    Yields:
    str: Chunks of the assistant's response.
    """
    # Prepare the request payload
    payload = {
        "query": query,
        "web_search": web_search
    }

    try:
        # Send a POST request to the API
        with requests.post(api_url, json=payload, stream=True) as response:
            # Check if the request was successful
            response.raise_for_status()

            # Process the streamed response
            for line in response.iter_lines(decode_unicode=True):
                if line:
                    try:
                        json_response = json.loads(line)
                        if 'content' in json_response:
                            yield json_response['content']
                        elif 'error' in json_response:
                            yield f"Error: {json_response['error']}"
                    except json.JSONDecodeError:
                        yield f"Error decoding JSON: {line}"

    except requests.RequestException as e:
        yield f"Error making request: {str(e)}"

# Example usage
if __name__ == "__main__":
    user_query = "python code to sum two numpy arrays"
    for chunk in stream_chat(user_query):
        print(chunk, end='', flush=True)
    print()  # Print a newline at the end