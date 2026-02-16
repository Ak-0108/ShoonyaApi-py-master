import requests
import json

api_url = "http://mstocktrade.in/api/nifty_breakout.php" # Example API URL

response = requests.get(api_url)

if response.status_code == 200:
    data = response.json()
    for m in data:
        print(m)
        print(m['Low_Support'])
    print("Parsed JSON data:")
    #print(json.dumps(data, indent=2)) # Pretty-print for readability
else:
    print(f"Error: Could not retrieve data. Status code: {response.status_code}")

web_url=""
response = requests.get(web_url)

if response.status_code == 200:
    data = response
    for m in data:
        print(m)       
else:
    print(f"Error: Could not retrieve data. Status code: {response.status_code}")


