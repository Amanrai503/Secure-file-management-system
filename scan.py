import requests
import time
from dotenv import load_dotenv
import os

# Load API key from .env file (recommended for security)
load_dotenv()
API_KEY = os.getenv("api")

def scan_file_virustotal(file_path):
    url = "https://www.virustotal.com/api/v3/files"
    headers = {"x-apikey": API_KEY}

    with open(file_path, "rb") as file:
        files = {"file": (file_path, file)}
        response = requests.post(url, headers=headers, files=files)

    response_json = response.json()
    analysis_id = response_json.get("data", {}).get("id")

    if analysis_id:
        print(f"File uploaded successfully. Analysis ID: {analysis_id}")
        return get_scan_results(analysis_id)
    else:
        print("Error uploading file:", response_json)
        return None

def get_scan_results(analysis_id):
    url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
    headers = {"x-apikey": API_KEY}

    print("Waiting for analysis...")
    time.sleep(10)  # Wait a few seconds before fetching results

    response = requests.get(url, headers=headers)
    result = response.json()

    # Extract scan details
    stats = result.get("data", {}).get("attributes", {}).get("stats", {})
    malicious = stats.get("malicious", 0)
    suspicious = stats.get("suspicious", 0)
    undetected = stats.get("undetected", 0)

    print(f"Scan Results:\n- Malicious: {malicious}\n- Suspicious: {suspicious}\n- Undetected: {undetected}")

    if malicious > 0:
        print("⚠️ WARNING: This file is detected as malicious!")
    elif suspicious > 0:
        print("⚠️ This file is marked as suspicious.")
    else:
        print("✅ The file appears to be clean.")

    return result
#file_path = r"resources\icons8-delete-96.png"
#scan_file_virustotal(file_path)