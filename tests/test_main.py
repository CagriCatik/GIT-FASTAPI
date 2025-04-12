import pytest
from fastapi.testclient import TestClient
from api.main import app, FEATURE_GOODBYE, FEATURE_FORMAL_GREETING

client = TestClient(app)

def test_hello_default():
    response = client.get("/hello")
    assert response.status_code == 200
    # The greeting depends on the state of the FEATURE_FORMAL_GREETING flag.
    expected = "Good day Kraken" if FEATURE_FORMAL_GREETING else "Hello Kraken"
    assert response.json() == {"message": expected}

def test_hello_with_name():
    response = client.get("/hello", params={"name": "Alice"})
    assert response.status_code == 200
    expected = "Good day Alice" if FEATURE_FORMAL_GREETING else "Hello Alice"
    assert response.json() == {"message": expected}

def test_hello_formal_param():
    # Even if FEATURE_FORMAL_GREETING is off, the 'formal' query parameter should trigger a formal greeting.
    response = client.get("/hello", params={"formal": True})
    assert response.status_code == 200
    assert response.json()["message"].startswith("Good day")

# Only run tests for the /goodbye endpoint when FEATURE_GOODBYE is enabled.
@pytest.mark.skipif(not FEATURE_GOODBYE, reason="Goodbye endpoint disabled by feature flag")
def test_goodbye_default():
    response = client.get("/goodbye")
    assert response.status_code == 200
    assert response.json() == {"message": "Goodbye world"}

@pytest.mark.skipif(not FEATURE_GOODBYE, reason="Goodbye endpoint disabled by feature flag")
def test_goodbye_with_name():
    response = client.get("/goodbye", params={"name": "Alice"})
    assert response.status_code == 200
    assert response.json() == {"message": "Goodbye Alice"}
