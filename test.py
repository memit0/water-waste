import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from water_usage import fetch_water_data, save_to_db, query_db

class TestWaterUsage(unittest.TestCase):

    @patch('requests.get')
    def test_fetch_water_data(self, mock_get):
        # Sample data to be returned by the mock
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "result": {
                "records": [
                    {"ilce": "Kadikoy", "usage": 100},
                    {"ilce": "Besiktas", "usage": 150}
                ]
            }
        }
        mock_get.return_value = mock_response

        url = "https://data.ibb.gov.tr/api/3/action/datastore_search?resource_id=b742a205-1adb-4f99-8b04-6f3025feb404&limit=5"
        df = fetch_water_data(url)

        self.assertEqual(len(df), 2)
        self.assertIn('ilce', df.columns)
        self.assertIn('usage', df.columns)
    
    def test_save_to_db(self):
        df = pd.DataFrame([
            {"ilce": "Kadikoy", "usage": 100},
            {"ilce": "Besiktas", "usage": 150}
        ])
        engine = save_to_db(df)
        
        with engine.connect() as connection:
            result = connection.execute(db.text("SELECT * FROM waterist;")).fetchall()
            result_df = pd.DataFrame(result, columns=['index', 'ilce', 'usage'])
        
        self.assertEqual(len(result_df), 2)
        self.assertEqual(result_df.iloc[0]['ilce'], 'Kadikoy')
        self.assertEqual(result_df.iloc[1]['usage'], 150)

    def test_query_db(self):
        df = pd.DataFrame([
            {"ilce": "Kadikoy", "usage": 100},
            {"ilce": "Besiktas", "usage": 150}
        ])
        engine = save_to_db(df)
        
        result_df = query_db(engine)
        
        self.assertEqual(len(result_df), 2)
        self.assertEqual(result_df.iloc[0]['ilce'], 'Kadikoy')
        self.assertEqual(result_df.iloc[1]['usage'], 150)

if __name__ == '__main__':
    unittest.main()
