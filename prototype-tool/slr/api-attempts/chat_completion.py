import http.client
import json
import os
from dotenv import load_dotenv

load_dotenv()

conn = http.client.HTTPSConnection("chat.kiconnect.nrw")

MODEL = "mistral-small-3.2-24B-instruct-2506" #mixtral-8x22B, mistral-small-3.2-24B-instruct-2506, gpt-oss-120b
SYSTEM_ROLE = 'system'
SYSTEM_PROMPT = 'You are an academic paper reviewer assistant. Score papers 1-5 on worth reading, return JSON.'


payload = {
    "model": MODEL,
    "messages": [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Title: Attention is All You Need\nAbstract: This paper proposes the Transformer architecture for sequence modeling..."
        }
    ]
}

headers = {
    'Content-Type': "application/json",
    'Authorization': f"Bearer {os.getenv('RWTH_GPT_API_KEY')}"
}

payload = json.dumps(payload)

conn.request("POST", "/api/v1/chat/completions", payload, headers)

res = conn.getresponse()
data = res.read()

returned_content = json.loads(data.decode("utf-8"))['choices'][0]['message']['content']
returned_content = returned_content.replace("```json", "").replace("```", "")
returned_json = json.loads(returned_content)
print(returned_json)
print(returned_json['score'])
