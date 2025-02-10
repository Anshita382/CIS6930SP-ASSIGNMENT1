import sys
from unittest.mock import patch
import pytest
from main import fetch_crime_data

class TestCrimeDataFetching:

    @patch('main.requests.get')  # Ensure we patch the correct module
    def test_fetch_crime_data_failure(self, mock_get):
        """Test that the function handles failures properly by returning an empty list"""
        # Simulate a failure response (e.g., network failure or HTTP error)
        mock_get.side_effect = Exception("Request failed")

        api_url = "https://data.cityofgainesville.org/resource/gvua-xt9q.json"
        page_start = 0
        page_size = 10

        # Patch sys.stderr to prevent print output from breaking tests
        with patch('sys.stderr', new_callable=lambda: sys.stdout):
            response = fetch_crime_data(api_url, page_start, page_size)

        # Verify the function returns an empty list on failure
        assert response == []

    @patch('main.requests.get')
    def test_fetch_crime_data_success(self, mock_get):
        """Test successful data fetching and correct JSON parsing"""
        # Simulate a successful response with mock data
        mock_get.return_value.json.return_value = [{
            "narrative": "Test incident",
            "report_date": "2023-02-09",
            "offense_date": "2023-02-08",
            "latitude": 29.6516,
            "longitude": -82.3248
        }]

        api_url = "https://data.cityofgainesville.org/resource/gvua-xt9q.json"
        page_start = 0
        page_size = 10

        # Call the function and verify the result
        response = fetch_crime_data(api_url, page_start, page_size)

        # Expected result from the mock API
        expected_output = [{
            "narrative": "Test incident",
            "report_date": "2023-02-09",
            "offense_date": "2023-02-08",
            "latitude": 29.6516,
            "longitude": -82.3248
        }]

        # Verify that the response matches the mock data
        assert response == expected_output
