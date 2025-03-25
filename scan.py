import requests
import dotenv

API_KEY = "your_virustotal_api_key"

def scan_file_virustotal(file_path):
    url = "https://www.virustotal.com/api/v3/files"
    headers = {"x-apikey": API_KEY}
    
    with open(file_path, "rb") as file:
        files = {"file": (file_path, file)}
        response = requests.post(url, headers=headers, files=files)
    
    return response.json()

file_path = "D:\\path\\to\\file.exe"
print(scan_file_virustotal(file_path))