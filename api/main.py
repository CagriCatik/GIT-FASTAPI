import os
from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel, Field
from typing import Dict, List, Optional

app = FastAPI()

# Feature flags controlled via environment variables.
FEATURE_GOODBYE = os.environ.get("FEATURE_GOODBYE", "True") == "True"
FEATURE_FORMAL_GREETING = os.environ.get("FEATURE_FORMAL_GREETING", "False") == "True"

# -----------------------------
# Existing Endpoints (GET)
# -----------------------------

@app.get("/hello")
def read_hello(name: Optional[str] = None, formal: bool = False):
    """
    GET endpoint that returns a greeting message.
    
    Query Parameters:
    - name (optional): A custom name for a personalized greeting.
    - formal (optional): When True, the endpoint returns a formal greeting. 
                         This parameter always overrides the default behavior.
                         
    If FEATURE_FORMAL_GREETING is enabled via environment variable, all greetings default to formal.
    """
    if formal or FEATURE_FORMAL_GREETING:
        greeting = "Good day"
    else:
        greeting = "Hello"
    
    if name:
        greeting += f" {name}"
    else:
        greeting += " Kraken"
    
    return {"message": greeting}

if FEATURE_GOODBYE:
    @app.get("/goodbye")
    def read_goodbye(name: Optional[str] = "world"):
        """
        GET endpoint that returns a farewell message.
        
        Query Parameters:
        - name (optional): Specifies a custom name for a personalized farewell.
        
        Uses the default name 'world' if not provided.
        """
        return {"message": f"Goodbye {name}"}

# -----------------------------
# New Endpoints: CRUD for Messages
# -----------------------------

class Message(BaseModel):
    id: Optional[int] = Field(None, example=1)
    content: str = Field(..., example="This is a sample message.")

# In-memory store for messages.
messages: Dict[int, Message] = {}
next_message_id = 1

@app.get("/messages", response_model=List[Message])
def list_messages():
    """
    GET /messages
    Returns a list of all messages.
    """
    return list(messages.values())

@app.get("/messages/{message_id}", response_model=Message)
def get_message(message_id: int = Path(..., title="Message ID", description="The ID of the message to retrieve", ge=1)):
    """
    GET /messages/{message_id}
    Returns a single message specified by its ID.
    """
    if message_id not in messages:
        raise HTTPException(status_code=404, detail="Message not found")
    return messages[message_id]

@app.post("/messages", response_model=Message, status_code=201)
def create_message(message: Message):
    """
    POST /messages
    Creates a new message and returns it with an assigned ID.
    """
    global next_message_id
    message.id = next_message_id
    messages[next_message_id] = message
    next_message_id += 1
    return message

@app.put("/messages/{message_id}", response_model=Message)
def update_message(message_id: int, updated_message: Message):
    """
    PUT /messages/{message_id}
    Fully updates an existing message.
    
    The message's content is replaced with the new content provided.
    """
    if message_id not in messages:
        raise HTTPException(status_code=404, detail="Message not found")
    updated_message.id = message_id
    messages[message_id] = updated_message
    return updated_message

@app.patch("/messages/{message_id}", response_model=Message)
def partially_update_message(message_id: int, message_update: dict):
    """
    PATCH /messages/{message_id}
    Partially updates an existing message.
    
    Only the provided fields will be updated.
    """
    if message_id not in messages:
        raise HTTPException(status_code=404, detail="Message not found")
    stored_message_data = messages[message_id].dict()
    stored_message_data.update(message_update)
    updated_message = Message(**stored_message_data)
    messages[message_id] = updated_message
    return updated_message

@app.delete("/messages/{message_id}", status_code=204)
def delete_message(message_id: int):
    """
    DELETE /messages/{message_id}
    Deletes a message by its ID.
    """
    if message_id not in messages:
        raise HTTPException(status_code=404, detail="Message not found")
    del messages[message_id]
