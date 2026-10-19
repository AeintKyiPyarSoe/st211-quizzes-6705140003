import pytest

@pytest.fixture(scope="session")
def expensive_setup():
    print("\n[session] expensive setup runs ONCE")
    return {"config": "loaded"}

def test_a(expensive_setup):
    assert expensive_setup["config"] == "loaded"
    
def test_b(expensive_setup):
    assert "config" in expensive_setup

