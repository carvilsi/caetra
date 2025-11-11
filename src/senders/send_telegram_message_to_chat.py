import requests
import json

BOT_API_KEY = 
CHAT_ID = 
URL = f"https://api.telegram.org/bot{BOT_API_KEY}/sendMessage"
HEADERS = {"Content-Type": "application/json"}

print(URL)

data = {
    "chat_id": f"{CHAT_ID}", 
    "text": "The world is all that is the case"
} 

print(data)
try:
    response = requests.post(URL, headers=HEADERS, json=data)
    print("Status Code", response.status_code)
    print("Response", response.json())
except requests.exceptions.HTTPError as errh:
    print("Error HTTP: " + str(errh)) 
except requests.exceptions.RequestException as errex:
    print("Error Request: " + str(errex)) 
except Exception as e:
    print("Error: " + str(e))
          
