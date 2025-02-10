from unittest.mock import patch
import pytest
from main import fetch_crime_data

class TestCrimeDataFetching:

    @patch('main.requests.get')
    def test_fetch_crime_data_failure(self, mock_get):
        # Simulate a failure response (e.g., 404 error or connection issue)
        mock_get.side_effect = Exception("Request failed")

        api_url = "https://data.cityofgainesville.org/resource/gvua-xt9q.json"
        page_start = 0
        page_size = 10

        # Call the function and check if it returns an empty list
        response = fetch_crime_data(api_url, page_start, page_size)

        # Verify that the response is an empty list
        assert response == []

    @patch('main.requests.get')
    def test_fetch_crime_data_success(self, mock_get):
        # Simulate a successful response with mock data
        mock_get.return_value.json.return_value = [{"narrative": "Test incident", "report_date": "2023-02-09", "offense_date": "2023-02-08", "latitude": 29.6516, "longitude": -82.3248}]

        api_url = "https://data.cityofgainesville.org/resource/gvua-xt9q.json"
        page_start = 0
        page_size = 10

        # Call the function and verify the result
        response = fetch_crime_data(api_url, page_start, page_size)

        # Verify the result matches the expected mock data
        assert response == [{"narrative": "Test incident", "report_date": "2023-02-09", "offense_date": "2023-02-08", "latitude": 29.6516, "longitude": -82.3248}]

