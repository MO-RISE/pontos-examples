import requests

print(
    "The request is limited to the first 100 rows in this example. "
    "The full day is ~50MB of data. Have a look at line 23 in the "
    "code if you want to change this."
)

TOKEN = input("Please input your PONTOS HUB token: ")

BASE_URL = "https://pontos.ri.se/api"

PATH = "vessel_data"

# Build the query using the syntax specified by PostgREST, for details see here:
# https://postgrest.org/en/stable/references/api/tables_views.html
# For details about the table layout, please refer to:
# https://pontos.ri.se/docs
query = (
    "select=time,parameter_id,value::float"  # The columns we want to fetch, casting value to float
    "&time=gte.2023-08-15&time=lt.2023-08-16"  # Filtering on time
    "&vessel_id=eq.name_sedna"  # Filtering on vessel_id
    "&limit=100"  # Limiting the number of rows may be a good way of speeding up trialling queries
)


# Build the headers
headers = {"Authorization": f"Bearer {TOKEN}"}

# Make the request and check for errors
response = requests.get(f"{BASE_URL}/{PATH}?{query}", headers=headers)
response.raise_for_status()

# Save to file
with open("single_day.json", mode="w") as fhandle:
    fhandle.write(response.text)
