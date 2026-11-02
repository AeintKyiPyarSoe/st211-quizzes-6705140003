def get_temperature(): # get_temperature() is a function that returns the current temperature. In a real-world scenario, it might fetch data from a weather API or sensor. For testing purposes, we can mock this function to return specific values.
    return 20

def describe_weather():
    if get_temperature() >= 15:
        return "Pleasant"
    return "Cold"