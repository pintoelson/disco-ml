import os
import requests
import json
from datetime import datetime

def load_dotenv(dotenv_path=".env"):
    """Manually load .env variables."""
    if os.path.exists(dotenv_path):
        with open(dotenv_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip().strip('"').strip("'")

def probe_key(api_key, label, base_url):
    """Probe an API key for models and rate limits."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    results = []
    
    # 1. Fetch available models
    print(f"[{label}] Fetching models...")
    try:
        resp = requests.get(f"{base_url}/models", headers=headers, timeout=10)
        models_data = resp.json().get("data", [])
        model_ids = [m["id"] for m in models_data]
    except Exception as e:
        print(f"[{label}] Error fetching models: {e}")
        return []

    # 2. Probe each model
    for model_id in model_ids:
        print(f"[{label}] Probing model: {model_id}...")
        payload = {
            "model": model_id,
            "messages": [{"role": "user", "content": "hi"}],
            "max_tokens": 1
        }
        
        try:
            resp = requests.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=10)
            
            # Extract rate limit headers (OpenAI style)
            limits = [v for k, v in resp.headers.items() if 'ratelimit' in k.lower()]
            limit_str = "; ".join(limits) if limits else "Not Reported"
            
            # Check for error message limits (some APIs return limits in error msg 429)
            status_text = "Accessible"
            if resp.status_code == 429:
                status_text = f"Rate Limited: {resp.text[:50]}"
            elif resp.status_code != 200:
                status_text = f"Error {resp.status_code}"

            results.append({
                "Key Type": label,
                "Model ID": model_id,
                "Status": status_text,
                "Rate Limit (Headers)": limit_str,
                "Response Code": resp.status_code
            })
        except Exception as e:
            results.append({
                "Key Type": label,
                "Model ID": model_id,
                "Status": f"Probe Failed: {str(e)[:50]}",
                "Rate Limit (Headers)": "N/A",
                "Response Code": "Error"
            })
            
    return results

def generate_markdown(results):
    """Generate markdown table from results."""
    md = "# RWTH GPT API Diagnostic Report\n\n"
    md += f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    md += "| Key Type | Model ID | Status | Rate Limit (Headers) | Code |\n"
    md += "| :--- | :--- | :--- | :--- | :--- |\n"
    
    for r in results:
        md += f"| {r['Key Type']} | `{r['Model ID']}` | {r['Status']} | {r['Rate Limit (Headers)']} | {r['Response Code']} |\n"
    
    md += "\n## Note on Rate Limits\n"
    md += "If 'Not Reported' is shown, the API does not expose rate limits through standard headers. "
    md += "Limits may be enforced silently or via specific account dashboard only.\n"
    
    return md

def main():
    load_dotenv()
    
    student_key = os.getenv("RWTH_GPT_API_KEY")
    employee_key = os.getenv("RWTH_GPT_EMP_API_KEY")
    base_url = "https://chat.kiconnect.nrw/api/v1"
    
    all_results = []
    
    if student_key:
        all_results.extend(probe_key(student_key, "Student", base_url))
    else:
        print("Student key not found in .env")

    if employee_key:
        all_results.extend(probe_key(employee_key, "Employee", base_url))
    else:
        print("Employee key not found in .env")

    if all_results:
        report_md = generate_markdown(all_results)
        with open("api_report.md", "w") as f:
            f.write(report_md)
        print("\nDiagnostic report generated: api_report.md")
        print("\n--- REPORT PREVIEW ---")
        print(report_md)
    else:
        print("No results to report.")

if __name__ == "__main__":
    main()
