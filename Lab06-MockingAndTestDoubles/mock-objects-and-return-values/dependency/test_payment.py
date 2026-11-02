from unittest.mock import Mock
from payment import OrderProcessor

def test_order_processing():
    # Create a mock payment gateway
    fake_gateway = Mock() # used mock to simulate the behavior of the PaymentGateway class without needing a real implementation. This allows us to test the OrderProcessor class in isolation.
    fake_gateway.charge.return_value = "SUCCESS-12345" # the return transaction ID
    
    processor =OrderProcessor(fake_gateway) # check if OrderProcessor calls the payment gateway
    result = processor.process(100)
    
    assert result == "Order processed: SUCCESS-12345" # check if the return transaction ID is used correctly
    # check ifthe final message is formatted as expected.
    
