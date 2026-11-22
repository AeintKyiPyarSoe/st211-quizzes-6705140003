from shipping import calculate_shipping

def test_basic_shipping():
    assert calculate_shipping(10) == 20
    
def test_express_shipping():
    assert calculate_shipping(10, express=True) == 30
    
