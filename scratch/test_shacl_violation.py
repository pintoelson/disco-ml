import json
import requests

BACKEND_URL = "http://localhost:8000/test/upload-ticket"

dummy_ticket = {
    "version_id": "dummy_ticket_v4_datatype_fail",
    "author": "Tester",
    "timestamp": "not-a-date",
    "status": "Test",
    "schema_data": {
        "Issue": "Check if validation is still on",
        "Decision": "Invalid date",
        "Rationale": "Testing"
    }
}

def test():
    r = requests.post(BACKEND_URL, json=dummy_ticket)
    print(f"Status: {r.status_code}")
    print(f"Body: {r.text}")

if __name__ == "__main__":
    test()
