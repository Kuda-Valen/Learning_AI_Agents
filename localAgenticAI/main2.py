import requests
import json
import shutil

OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"

# ==========================================
# 1. ACTUAL AGENT TOOLS (Python Functions)
# ==========================================
def get_disk_usage(path: str = "/") -> dict:
    """Gets total, used, and free disk space for a path."""
    try:
        total, used, free = shutil.disk_usage(path)
        return {
            "status": "success",
            "path": path,
            "total_gb": round(total / (1024**3), 2),
            "used_gb": round(used / (1024**3), 2),
            "free_gb": round(free / (1024**3), 2)
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Map LLM actions to executable functions
TOOL_REGISTRY = {
    "check_disk": get_disk_usage
}

# ==========================================
# 2. LLM BRAIN (Decision Engine)
# ==========================================
def agent_brain(user_prompt: str, model_name: str = "qwen2.5:0.5b") -> dict:
    system_instruction = """
    You are an Autonomous System Agent. 
    Analyze the user prompt and choose an action.
    Available Tools:
    - check_disk: Use this to check disk space. Requires "path" argument (e.g., "/").
    
    Return ONLY a JSON response:
    {"tool": "check_disk" | "none", "args": {"path": string}}
    """

    payload = {
        "model": model_name,
        "prompt": f"{system_instruction}\nUser: {user_prompt}\nJSON Response:",
        "stream": False,
        "format": "json"
    }

    response = requests.post(OLLAMA_ENDPOINT, json=payload)
    result = response.json()
    
    if "error" in result:
        raise Exception(f"Ollama Error: {result['error']}")

    return json.loads(result["response"])

# ==========================================
# 3. REACT EXECUTION LOOP
# ==========================================
def run_react_agent(user_prompt: str):
    print(f"\n[USER]: {user_prompt}")
    
