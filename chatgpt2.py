import requests
import os
import time

API_URL = "https://api.mem.ai/v0/mems"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "ApiAccessToken <put_here_your_access_token>"
}

# Define custom beggining line / title in mem.ai
CUSTOM_LINE = "CHATGPT "

def post_mem(content):
    data = {
        "content": content
    }
    response = requests.post(API_URL, json=data, headers=HEADERS)
    if response.status_code == 429:  # Rate limit reached
        print("Rate limited. Waiting for 60 seconds...")
        time.sleep(60)
        return post_mem(content)
    elif response.status_code != 200:
        print(f"Error encountered: {response.status_code} - {response.text}")
        return None
    try:
        return response.json()
    except Exception as e:
        print(f"Error parsing response: {e}")
        return None

directory_path = "./formatted_conversations"
files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f)) and f.endswith('.txt')]

for file_name in files:
    file_path = os.path.join(directory_path, file_name)
    with open(file_path, 'r', encoding="utf-8") as file:
        content = file.read()
        # Add custom line
        full_content = CUSTOM_LINE + content
        print(f"Processing file: {file_path}")
        response = post_mem(full_content)
        if response:
            print(response)
