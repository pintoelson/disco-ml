import http.client
import ssl
import json
import os
import time
from utils import create_payload

def call_rwth_gpt_api(model, system_role, system_prompt, prompt_template, prompt_data, inclusion_criteria, exclusion_criteria):
    messages = create_payload(model, system_role, system_prompt, prompt_template, prompt_data, inclusion_criteria, exclusion_criteria)
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0,
    }
    if model not in ('mixtral-8x22B', 'mistral-small-3.2-24B-instruct-2506', 'gpt-oss-120b'): api_key = os.getenv('RWTH_GPT_API_KEY_EMP')
    else: api_key = os.getenv('RWTH_GPT_API_KEY')
    
    context = ssl._create_unverified_context()
    conn = http.client.HTTPSConnection("chat.kiconnect.nrw", context=context)
    headers = {
        'Content-Type': "application/json",
        'Authorization': f"Bearer {api_key}"
    }

    payload_json = json.dumps(payload)
    conn.request("POST", "/api/v1/chat/completions", payload_json, headers)

    res = conn.getresponse()
    data = res.read()
    returned_content = json.loads(data.decode("utf-8"))['choices'][0]['message']['content']
    returned_content = returned_content.replace("```json", "").replace("```", "").strip()
    returned_json = json.loads(returned_content)
    
    return returned_json

def call_gemini_api(model, system_role, system_prompt, prompt_template, prompt_data, inclusion_criteria, exclusion_criteria):
    # time.sleep(4)
    prompt_content = prompt_template.format(INCLUSION_CRITERIA=inclusion_criteria, 
                                          EXCLUSION_CRITERIA=exclusion_criteria, 
                                          TITLE=prompt_data['title'], 
                                          ABSTRACT=prompt_data['abstract'])
    
    payload = {
        "contents": [{"parts": [{"text": prompt_content}]}],
        "system_instruction": {"parts": [{"text": system_prompt}]},
        "generationConfig": {
            "temperature": 0,
            "response_mime_type": "application/json"
        }
    }

    api_key = os.getenv('GEMINI_API_KEY')
    conn = http.client.HTTPSConnection("generativelanguage.googleapis.com")
    headers = {'Content-Type': "application/json"}
    
    endpoint = f"/v1beta/models/{model}:generateContent?key={api_key}"
    payload_json = json.dumps(payload)

    conn.request("POST", endpoint, payload_json, headers)

    res = conn.getresponse()
    data = res.read()
    response_json = json.loads(data.decode("utf-8"))
    
    try:
        print(f'Successful gemini call for {prompt_data.get("title")[:30]}...')
        returned_content = response_json['candidates'][0]['content']['parts'][0]['text']
        returned_content = returned_content.replace("```json", "").replace("```", "").strip()
        returned_json = json.loads(returned_content)
        return returned_json
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Error parsing Gemini response: {e}")
        # print(f"Raw Response: {json.dumps(response_json, indent=2)}")
        return {
            "summary": "Error calling Gemini API",
            "decision": "Uncertain",
            "matched_ic": [],
            "triggered_ec": [],
            "justification": f"API Error or invalid response format: {str(e)}",
            "score": 0.0
        }

def call_groq_api(model, system_role, system_prompt, prompt_template, prompt_data, inclusion_criteria, exclusion_criteria):
    # time.sleep(4)
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return {"summary": "Error: GROQ_API_KEY missing", "decision": "Uncertain", "matched_ic": [], "triggered_ec": [], "justification": "API Key missing", "score": 0.0}
    
    payload = {
        "model": model,
        "messages": [
            {"role": system_role, "content": system_prompt},
            {"role": "user", "content": prompt_template.format(
                TITLE=prompt_data['title'],
                ABSTRACT=prompt_data['abstract'],
                INCLUSION_CRITERIA=inclusion_criteria,
                EXCLUSION_CRITERIA=exclusion_criteria
            )}
        ],
        "temperature": 0.0,
        "response_format": {"type": "json_object"}
    }
    
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    conn = http.client.HTTPSConnection("api.groq.com")
    conn.request("POST", "/openai/v1/chat/completions", json.dumps(payload), headers)
    
    res = conn.getresponse()
    data = res.read()
    response_json = json.loads(data.decode("utf-8"))
    
    try:
        print(f'Successful Groq call for {prompt_data.get("title")[:30]}...')
        returned_content = response_json['choices'][0]['message']['content']
        returned_content = returned_content.replace("```json", "").replace("```", "").strip()
        returned_json = json.loads(returned_content)
        return returned_json
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print(f"Error parsing Groq response: {e}")
        # print(f"Raw Response: {json.dumps(response_json, indent=2)}")
        # Get header response
        # print(f"Response Headers: {res.headers}")
        retry_after = res.headers.get('Retry-After')
        if retry_after:
            print(f"Retry after: {retry_after}")
            time.sleep(int(retry_after) + 1)
            return call_groq_api(model, system_role, system_prompt, prompt_template, prompt_data, inclusion_criteria, exclusion_criteria)
        return {
            "summary": "Error calling Groq API",
            "decision": "Uncertain",
            "matched_ic": [],
            "triggered_ec": [],
            "justification": f"API Error or invalid response format: {str(e)}",
            "score": 0.0
        }
