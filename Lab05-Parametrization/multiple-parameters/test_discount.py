import pytest
from discount import apply_discount

@pytest.mark.parametrize("price,percent,expected", [
    (100,0,100), # no discount
    (100,50,50), # 50% discount
    (100,100,0), # 100% discount
    (200,25,150), # 25% discount
    (50,10,45), # 10% discount
    (80,10,72), # 10% discount
])

def test_apply_discount_calculation(price, percent, expected):
    assert apply_discount(price, percent) == expected