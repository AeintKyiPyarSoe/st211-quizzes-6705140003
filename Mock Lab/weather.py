import random

def get_temperature():
    """Simulate getting the current temperature in Celsius."""
    return random.randint(-10, 40)  # Random temperature between -10 and 40 degrees Celsius, mock data for testing purposes

def describe_weather():
    temp = get_temperature()
    if temp < 0:
        return "Freezing"
    elif temp < 15:
        return "Cold"
    elif temp < 25:
        return "Pleasant"
    else:
        return "Hot"