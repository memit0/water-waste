import requests
import sqlalchemy as db
import pandas as pd

url = "https://data.ibb.gov.tr/api/3/action/datastore_search?resource_id=b742a205-1adb-4f99-8b04-6f3025feb404&limit=5"

response = requests.get(url)

if response.status_code == 200:
  data = response.json()
  records = data.get('result', {}).get('records', [])
  waterist = pd.DataFrame.from_dict(records)
else:
  print(f"Request failed with status code: {response.status_code}")

if not waterist.empty:
    engine = db.create_engine('sqlite:///waterist.db')

    waterist.to_sql('waterist', con=engine, if_exists='replace', index=False)

    with engine.connect() as connection:
        query_result = connection.execute(db.text("SELECT * FROM waterist;")).fetchall()
        query_df = pd.DataFrame(query_result, columns=waterist.columns)
        table = query_df[['Ilce'] + [col for col in query_df.columns if col != 'Ilce']]
        print(table)
else:
    print("No data available.")