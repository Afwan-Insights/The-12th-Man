from fastapi.testclient import TestClient
from main import app  # This imports your FastAPI app from main.py

client = TestClient(app)

def test_root_endpoint():
    # If you have a root endpoint serving the frontend, test it
    response = client.get("/")
    assert response.status_code == 200

def test_telemetry_data():
    # Testing your specific wait-times endpoint
    response = client.get("/api/telemetry/wait-times")
    
    # Check that the server responds successfully
    assert response.status_code == 200
    
    # Check that the server is returning a JSON response (like a dictionary or list)
    assert isinstance(response.json(), (dict, list))
    def test_invalid_sos_report_security():
        # Intentionally sending a bad payload (missing the 'zone', and 'urgency' is too high)
        bad_payload = {
            "issue_type": "Medical Emergency",
            "urgency": 10  # This should fail because max urgency is 5
        }
        response = client.post("/api/sos-report", json=bad_payload)
        
        # We explicitly EXPECT a 422 error because our Pydantic validation blocked it
        assert response.status_code == 422