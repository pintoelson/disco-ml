import json
import requests

BACKEND_URL = "http://localhost:8000/test/upload-ticket"

dummy_ticket = {
    "version_id": "dummy_ticket_class_fail",
    "filename": "dummy_ticket_v3.json",
    "author": "Tester",
    "timestamp": "2023-10-27T10:00:00",
    "status": "Test",
    "schema_data": {
        "Issue": "Testing SHACL class validation",
        "Decision": "Author is an Animal",
        "Rationale": "Verify if sh:class is enforced"
    }
}

def test_class_validation():
    print("Uploading ticket where author is a schema:Animal...")
    try:
        response = requests.post(BACKEND_URL, json=dummy_ticket)
        if response.status_code == 200:
            print("  SUCCESS (SHACL class validation did not trigger!)")
        else:
            print(f"  FAILED as expected ({response.status_code})")
            print(f"  Detail: {response.text}")
    except Exception as e:
        print(f"  Error: {e}")

if __name__ == "__main__":
    test_class_validation()
