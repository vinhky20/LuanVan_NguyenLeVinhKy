import requests

response = requests.get("http://localhost:5000/services")
data = response.json()
for x in data:
    if (x['SERVICE_NAME'] == "Chữa tuỷ răng"):
        idService = x['SERVICE_ID']
print(idService)
