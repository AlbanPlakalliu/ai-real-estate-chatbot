from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    role: str
    content: str
    timestamp: Optional[datetime] = None

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    user_id: Optional[int] = None
    conversation_history: Optional[List[ChatMessage]] = []

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    suggested_properties: Optional[List[int]] = []
    extracted_preferences: Optional[dict] = None

class Conversation(BaseModel):
    id: str
    user_id: Optional[int] = None
    messages: List[ChatMessage]
    created_at: datetime
    updated_at: datetime
    
class ConversationList(BaseModel):
    conversations: List[Conversation]
    total: int