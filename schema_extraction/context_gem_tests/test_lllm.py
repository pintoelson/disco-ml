import litellm
import os
from dotenv import load_dotenv

load_dotenv()

# Set your API key
# print(os.environ["RWTH_GPT_API_KEY"])

# Chat completions
response = litellm.completion(
    model="rwth_gpt/gpt-oss-120b",
    messages=[{"role": "user", "content": "Hello"}],
)

print(response)

# Responses API (if supported_endpoints includes "/v1/responses")
response = litellm.responses(
    model="rwth_gpt/gpt-oss-120b",
    input="Hello",
)

print(response)