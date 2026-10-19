import pytest

class FakeDatabase:
    def __init__(self):
        self.connected = False
        self.data = []
    def connect(self):
        self.connected = True
    def disconnect(self):
        self.connected = False
        
@pytest.fixture
def database():
    db = FakeDatabase()
    db.connect() # setup
    yield db
    db.disconnect() # teardown

def test_database_connected(database):
    assert database.connected is True