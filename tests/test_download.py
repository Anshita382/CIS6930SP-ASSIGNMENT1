import sys
from unittest.mock import patch
import pytest
import requests
from main import fetch_crime_data, main

class TestCrimeDataFetching:

    @patch('main.requests.get')  # Ensure we patch the correct module
    def test_fetch_crime_data_failure(self, mock_get):
        """Test that the function handles failures properly by returning an empty list"""
        mock_get.side_effect = requests.exceptions.RequestException("Request failed")

        api_url = "https://data.cityofgainesville.org/resource/gvua-xt9q.json"
        page_start = 0
        page_size = 10

        with patch('sys.stderr', new_callable=lambda: sys.stdout):
            response = fetch_crime_data(api_url, page_start, page_size)

        assert response == []

    @patch('main.requests.get')
    def test_fetch_crime_data_success(self, mock_get):
        """Test successful data fetching and correct JSON parsing"""
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

        response = fetch_crime_data(api_url, page_start, page_size)

        expected_output = [{
            "narrative": "Test incident",
            "report_date": "2023-02-09",
            "offense_date": "2023-02-08",
            "latitude": 29.6516,
            "longitude": -82.3248
        }]

        assert response == expected_output

    @patch("sys.argv", ["main.py", "--url", "https://data.cityofgainesville.org/resource/gvua-xt9q.json", "--offset", "0", "--limit", "5"])
    def test_main_script_execution(self):
        """Test the main function by simulating command-line arguments"""
        with patch("sys.stdout", new_callable=lambda: sys.stderr):  # Capture print output
            main()
