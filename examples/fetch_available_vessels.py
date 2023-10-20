import requests

TOKEN = input("Please input your PONTOS HUB token: ")

BASE_URL = "https://pontos.ri.se/api"

PATH = "vessel_ids"

# Build the headers
headers = {"Authorization": f"Bearer {TOKEN}"}

# Make the request and check for errors
response = requests.get(f"{BASE_URL}/{PATH}", headers=headers)
response.raise_for_status()

# Print to console

print(response.text)