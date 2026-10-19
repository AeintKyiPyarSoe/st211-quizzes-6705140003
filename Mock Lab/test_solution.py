from unittest.mock import patch
from weather import describe_weather

def test_hot_weather():
    with patch('weather.get_temperature', return_value=30):  # Mock get_temperature to return 30
        assert describe_weather() == "Hot"

def test_freezing_weather():
    with patch('weather.get_temperature', return_value=-5):  # Mock get_temperature to return -5
        assert describe_weather() == "Freezing"

def test_cold_weather():
    with patch('weather.get_temperature', return_value=5):  # Mock get_temperature to return 5
        assert describe_weather() == "Cold"

def test_pleasant_weather():
    with patch('weather.get_temperature', return_value=20):  # Mock get_temperature to return 20
        assert describe_weather() == "Pleasant"
        
        
'''Control the dependency (get_temperature) 
to return specific values, allowing us 
to test the describe_weather function's behavior under different temperature conditions.
'''