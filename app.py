from flask import Flask, jsonify, render_template
from flask_cors import CORS
import requests
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home_page():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')


def fetch_water_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        records = data['result']['records']
        return pd.DataFrame(records)
    else:
        return pd.DataFrame()

@app.route('/api/water-usage', methods=['GET'])
def get_water_usage():
    url = "https://data.ibb.gov.tr/api/3/action/datastore_search?resource_id=b742a205-1adb-4f99-8b04-6f3025feb404&limit=5"
    try:
        df = fetch_water_data(url)
        records = df.to_dict(orient='records')
        return jsonify(records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
