import requests
CLIENT_ID = "6688259a-c570-4429-beb6-6fabc459fb58"
CLIENT_SECRET = "AcfYceEFPJtzTUXH"
def log_event(stack, level, package, message):
    url = "http://20.244.56.144/evaluation-service/logs"
    headers = {
        "Content-Type": "application/json",
        "Client-ID": CLIENT_ID,
        "Client-Secret": CLIENT_SECRET
    }
    payload = {
        "stack": stack.lower(),
        "level": level.lower(),
        "package": package.lower(),
        "message": message
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Log created successfully:", response.json()["logID"])
        else:
            print("Failed to log:", response.text)
    except Exception as e:
        print("Error sending log:", e)
