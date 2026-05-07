import json
import requests

BACKEND_URL = "http://localhost:8000/test/upload-ticket"

dummy_ticket = {
    "version_id": "dummy_ticket_wrong_class",
    "filename": "dummy_ticket_v2.json",
    "author": "Tester",
    "timestamp": "2023-10-27T10:00:00",
    "status": "Test",
    "schema_data": {
        "Issue": "Testing SHACL class validation",
        "Decision": "Connect to dd:Argument",
        "Rationale": "The builder now uses dd:Argument instead of sioc_arg:Argument",
        "Argument": [
            {
                "author": "Bob",
                "timestamp": "2023-10-27T11:00:00",
                "classification": "Pro",
                "argument": "This should fail because of wrong class"
            }
        ]
    }
}

def test_class_validation():
    print("Uploading ticket with argument having wrong class (dd:Argument)...")
    try:
        response = requests.post(BACKEND_URL, json=dummy_ticket)
        if response.status_code == 200:
            print("  SUCCESS (This is unexpected if SHACL is active and strict)")
        else:
            print(f"  FAILED as expected ({response.status_code})")
            print(f"  Detail: {response.text}")
    except Exception as e:
        print(f"  Error: {e}")

if __name__ == "__main__":
    test_class_validation()
