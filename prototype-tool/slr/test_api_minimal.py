import os
import json
from dotenv import load_dotenv
import sys

# Add current directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from api_handlers import call_gemini_api, call_groq_api
load_dotenv()

def test_gemini():
    model = "gemini-1.5-flash"
    system_role = "system"
    system_prompt = "You are a helpful assistant. Return JSON."
    prompt_template = "Return a JSON object with a 'test' field set to 'success'. Title: {TITLE}, Abstract: {ABSTRACT}, IC: {INCLUSION_CRITERIA}, EC: {EXCLUSION_CRITERIA}"
    prompt_data = {"title": "Test Title", "abstract": "Test Abstract"}
    inclusion_criteria = "Test IC"
    exclusion_criteria = "Test EC"

    print(f"Testing Gemini with model: {model}...")
    try:
        result = call_gemini_api(model, system_role, system_prompt, prompt_template, prompt_data, inclusion_criteria, exclusion_criteria)
        print("Result:", json.dumps(result, indent=2))
        if result.get("test") == "success" or "decision" in result:
            print("SUCCESS: Gemini API returned a valid response.")
    except Exception as e:
        print(f"ERROR: {e}")

def test_groq():
    model = "llama-3.1-8b-instant"
    system_role = "system"
    system_prompt = "You are a helpful assistant. Return JSON."
    prompt_template = "Return a JSON object with a 'test' field set to 'success'. Title: {TITLE}, Abstract: {ABSTRACT}, IC: {INCLUSION_CRITERIA}, EC: {EXCLUSION_CRITERIA}"
    prompt_data = {"title": "Test Title", "abstract": "Test Abstract"}
    inclusion_criteria = "Test IC"
    exclusion_criteria = "Test EC"

    print(f"Testing Groq with model: {model}...")
    try:
        result = call_groq_api(model, system_role, system_prompt, prompt_template, prompt_data, inclusion_criteria, exclusion_criteria)
        print("Result:", json.dumps(result, indent=2))
        if result.get("test") == "success" or "decision" in result:
            print("SUCCESS: Groq API returned a valid response.")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_gemini()
    test_groq()