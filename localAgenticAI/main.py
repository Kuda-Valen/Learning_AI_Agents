import os
import requests
import json

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"

# Updated model_name default to match installed 'qwen2.5:0.5b'
def query_local_agent(user_prompt: str, model_name: str = "qwen2.5:0.5b"):
    """ Executes an agent reasoning step using a locally hosted open-weight model """

    system_instruction = """
    You are a Local system Agent.
    Analyse the request and return ONLY a structured JSON response.
    Format: {"action": string, "target": string}
    """

    payload = {
        "model": model_name,
        "prompt": f"{system_instruction}\nUser: {user_prompt}\nJSON response: ",
        "stream": False,
        "format": "json"
    }

    response = requests.post(OLLAMA_ENDPOINT, json=payload)
    result = response.json()

    # Debug safety: check if server returned an error message
    if "error" in result:
        raise Exception(f"Ollama Server Error: {result['error']}")

    return json.loads(result["response"])

if __name__ == "__main__":

    try:
        user_prompt = input("Enter your prompt: ")
        agent_decision = query_local_agent(user_prompt)
        print(f"[LOCAL AGENT OUTPUT]: {agent_decision}")

    except Exception as e:
        print(f"Error connecting to local LLM runtime: {e}")