import http.client
import os
from dotenv import load_dotenv
import ssl
load_dotenv()

context = ssl._create_unverified_context()
conn = http.client.HTTPSConnection("chat.kiconnect.nrw", context=context)

headers = { 'Authorization': f"Bearer {os.getenv('RWTH_GPT_API_KEY')}" }

conn.request("GET", "/api/v1/models", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))