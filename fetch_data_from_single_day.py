import requests

TOKEN = input("Please input your PONTOS HUB token: ")

BASE_URL = "https://pontos.ri.se/api"

PATH = "vessel_data"

query = (
    "select=time,parameter_id,value::float"         # The columns we want to fetch
    "&time=gte.2023-08-15&time=lt.2023-08-16"       # Filtering on time
    "&vessel_id=eq.name_sedna"                      # Filtering on vessel_id
)


# Build the headers
headers = {"Authorization": f"Bearer {TOKEN}"}

# Make the request and check for errors
response = requests.get(f"{BASE_URL}/{PATH}?{query}", headers=headers)
response.raise_for_status()

# Save to file
with open("single_day.json", mode="w") as fhandle:
    fhandle.write(response.text)
