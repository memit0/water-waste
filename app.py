from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
import requests
import git
import pandas as pd

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home_page():
    return render_template('home.html', subtitle='Home Page', text='This is the home page')

@app.route("/update_server", methods=['POST'])
def webhook():
    if request.method == 'POST':
        repo = git.Repo('/home/istwaterusage/water-waste')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400


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
        return render_template('water.html', records=records)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
