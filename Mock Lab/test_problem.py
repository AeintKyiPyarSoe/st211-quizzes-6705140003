from weather import describe_weather

def test_get_weather():
    result = describe_weather() # call the function to get the weather description
    assert result in ["Freezing", "Cold", "Pleasant", "Hot"] # check that the result is one of the expected weather descriptions

'''
weak test, because weather is random, 
so it may not cover all cases. A better approach would be to mock the get_temperature function 
to return specific values and test the describe_weather function with those mocked values.
'''

    
    