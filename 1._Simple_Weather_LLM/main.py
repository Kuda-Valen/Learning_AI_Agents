import json

# ==========================================
# 1. THE TOOLS (Backend Functions)
# ==========================================
def get_weather(location: str, unit: str = "celsius") -> dict:
    """Mock weather API returning structured weather data."""
    mock_database = {
        "cape town": {"temperature": 18, "condition": "Sunny", "humidity": "60%"},
        "tokyo": {"temperature": 12, "condition": "Rainy", "humidity": "85%"},
        "london": {"temperature": 10, "condition": "Cloudy", "humidity": "75%"}
    }
    
    loc_key = location.lower()
    data = mock_database.get(loc_key, {"temperature": 20, "condition": "Clear", "humidity": "50%"})
    data["location"] = location
    data["unit"] = unit
    return data

# Map function names to executable Python functions
TOOL_REGISTRY = {
    "get_weather": get_weather
}

# Tool schemas passed to the LLM context window
TOOL_SCHEMAS = [
    {
        "name": "get_weather",
        "description": "Fetch current weather conditions for a given city.",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "The city name, e.g. Cape Town"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"], "default": "celsius"}
            },
            "required": ["location"]
        }
    }
]

# ==========================================
# 2. MOCK LLM ENGINE (Simulating Brain Logic)
# ==========================================
class SimulatedLLM:
    def parse_intent(self, user_prompt: str, tools: list) -> dict:
        """Simulates LLM analyzing prompt and outputting JSON decision."""
        prompt_lower = user_prompt.lower()
        
        # LLM Reasoning: Detects intent to query weather
        if "weather" in prompt_lower or "temperature" in prompt_lower:
            # Simple entity extraction simulation
            location = "Cape Town" if "cape town" in prompt_lower else "London" if "london" in prompt_lower else "Tokyo"
            
            return {
                "type": "function_call",
                "function": "get_weather",
                "arguments": {"location": location, "unit": "celsius"}
            }
        
        return {
            "type": "text_response",
            "content": "I am an AI assistant. How can I help you today?"
        }

    def summarize_observation(self, original_prompt: str, tool_result: dict) -> str:
        """Simulates final text synthesis after tool execution."""
        loc = tool_result["location"]
        temp = tool_result["temperature"]
        cond = tool_result["condition"]
        return f"The current weather in {loc} is {temp}°C with {cond.lower()} skies."

# ==========================================
# 3. THE AGENTIC EXECUTION LOOP
# ==========================================
def run_agentic_loop(user_prompt: str):
    print(f"\n[USER PROMPT]: '{user_prompt}'")
    llm = SimulatedLLM()
    
    # Step 1: Pass prompt & tool schemas to the LLM
    print("\n--- Step 1: Processing Prompt with LLM ---")
    llm_decision = llm.parse_intent(user_prompt, TOOL_SCHEMAS)
    
    # Step 2: Handle LLM Output
    if llm_decision["type"] == "function_call":
        func_name = llm_decision["function"]
        args = llm_decision["arguments"]
        
        print(f"[LLM DECISION]: Function Call Requested -> {func_name}()")
        print(f"[EXTRACTED ARGS]: {json.dumps(args)}")
        
        # Step 3: Execute tool from registry
        print("\n--- Step 2: Executing Tool in Backend Runtime ---")
        if func_name in TOOL_REGISTRY:
            tool_output = TOOL_REGISTRY[func_name](**args)
            print(f"[TOOL OUTPUT]: {json.dumps(tool_output)}")
            
            # Step 4: Return tool result back to LLM for final synthesis
            print("\n--- Step 3: Synthesizing Final Answer ---")
            final_response = llm.summarize_observation(user_prompt, tool_output)
            print(f"[AGENT RESPONSE]: {final_response}")
            return final_response
    else:
        print(f"[AGENT RESPONSE]: {llm_decision['content']}")
        return llm_decision['content']

# ==========================================
# 4. RUN SIMULATION
# ==========================================
if __name__ == "__main__":
    run_agentic_loop("What is the weather like in Cape Town today?")