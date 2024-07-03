import requests

url = "https://data.ibb.gov.tr/api/3/action/datastore_search?resource_id=b742a205-1adb-4f99-8b04-6f3025feb404&limit=5"

response = requests.get(url)

if response.status_code == 200:
  data = response.json()
  print(data)
else:
  print(f"Request failed with status code: {response.status_code}")