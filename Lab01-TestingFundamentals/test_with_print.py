def test_with_print():
    value = 42
    print(f"The value is {value}")
    assert value == 42