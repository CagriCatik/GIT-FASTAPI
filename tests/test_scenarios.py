from fastapi.testclient import TestClient
import pytest
from api.main import app, messages

client = TestClient(app)

def test_list_messages_empty():
    # Ensure the in-memory storage is empty
    messages.clear()
    response = client.get("/messages")
    assert response.status_code == 200
    assert response.json() == []

def test_create_and_get_message():
    # Create a new message
    response = client.post("/messages", json={"content": "Hello world!"})
    assert response.status_code == 201
    message = response.json()
    message_id = message["id"]
    
    # Retrieve that message
    get_response = client.get(f"/messages/{message_id}")
    assert get_response.status_code == 200
    assert get_response.json() == message

def test_update_message_with_put():
    # Create a message first
    response = client.post("/messages", json={"content": "Original"})
    message_id = response.json()["id"]
    
    # Update the message completely using PUT
    put_response = client.put(f"/messages/{message_id}", json={"content": "Updated complete message"})
    assert put_response.status_code == 200
    updated_message = put_response.json()
    assert updated_message["content"] == "Updated complete message"

def test_partially_update_message_with_patch():
    # Create a message first
    response = client.post("/messages", json={"content": "Initial content"})
    message_id = response.json()["id"]
    
    # Partial update using PATCH
    patch_response = client.patch(f"/messages/{message_id}", json={"content": "Partially updated message"})
    assert patch_response.status_code == 200
    assert patch_response.json()["content"] == "Partially updated message"

def test_delete_message():
    # Create a message first
    response = client.post("/messages", json={"content": "To be deleted"})
    message_id = response.json()["id"]
    
    # Delete the message
    delete_response = client.delete(f"/messages/{message_id}")
    assert delete_response.status_code == 204
    
    # Verify that the message has been deleted
    get_response = client.get(f"/messages/{message_id}")
    assert get_response.status_code == 404
