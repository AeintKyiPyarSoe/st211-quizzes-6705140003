import pytest

@pytest.fixture(params=["chrome", "firefox", "safari"])
def browser(request):
    browser_name = request.param
    print(f"\n [setup] Launching {browser_name}")
    yield browser_name  # This is where the test function will run
    print(f"\n [teardown] Closing {browser_name}")
    
def test_page_load(browser):
    assert browser is not None  # Just a dummy assertion to simulate a test (browser is a string, so we check that it's not None)
    
def test_browser_clickable(browser):
    assert len(browser) > 0  # Another dummy assertion to simulate a test (browser is a string, so we check its length)
    