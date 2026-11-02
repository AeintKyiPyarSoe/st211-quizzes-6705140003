from unittest.mock import patch
from weather import describe_weather

@patch("weather.get_temperature")
def test_pleasant_weather(mock_temp):
    mock_temp.return_value = 20 # here we patch get_temperature() to return 20, simulating a pleasant weather condition. This allows us to test the describe_weather() function without relying on the actual temperature.
    assert describe_weather() == "Pleasant"

@patch("weather.get_temperature")
def test_cold_weather(mock_temp):
    mock_temp.return_value = 5
    assert describe_weather() == "Cold"