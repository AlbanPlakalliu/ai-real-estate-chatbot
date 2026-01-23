from fastapi import APIRouter, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_service import ai_service
import uuid
from datetime import datetime

router = APIRouter()

# In-memory conversation storage (use Redis/DB in production)
CONVERSATIONS = {}

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Chat with AI assistant with conversation tracking"""
    try:
        # Generate or use existing conversation ID
        conv_id = request.conversation_id or str(uuid.uuid4())
        
        # Get conversation history
        history = []
        if conv_id in CONVERSATIONS:
            history = CONVERSATIONS[conv_id]
        
        # Add conversation history from request
        if request.conversation_history:
            history.extend([
                {"role": msg.role, "content": msg.content}
                for msg in request.conversation_history
            ])
        
        # Get AI response
        if ai_service:
            response_text = ai_service.chat(
                user_message=request.message,
                conversation_history=history
            )
        else:
            response_text = "AI service is unavailable."
        
        # Update conversation history
        history.append({"role": "user", "content": request.message})
        history.append({"role": "assistant", "content": response_text})
        CONVERSATIONS[conv_id] = history[-20:]  # Keep last 20 messages
        
        # Extract property preferences from conversation (simple keyword matching)
        suggested_property_ids = extract_property_suggestions(request.message, response_text)
        preferences = extract_preferences(request.message)
        
        return ChatResponse(
            response=response_text,
            conversation_id=conv_id,
            suggested_properties=suggested_property_ids,
            extracted_preferences=preferences
        )
        
    except Exception as e:
        print(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/conversations/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    if conversation_id not in CONVERSATIONS:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "conversation_id": conversation_id,
        "messages": CONVERSATIONS[conversation_id]
    }

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation"""
    if conversation_id in CONVERSATIONS:
        del CONVERSATIONS[conversation_id]
        return {"message": "Conversation deleted"}
    
    raise HTTPException(status_code=404, detail="Conversation not found")

def extract_property_suggestions(user_message: str, ai_response: str) -> list:
    """Extract property IDs that might interest the user"""
    # Simple keyword matching - in production use NLP
    keywords = user_message.lower()
    suggestions = []
    
    if "shoreditch" in keywords or "modern" in keywords:
        suggestions.append(1)
    if "camden" in keywords or "victorian" in keywords or "family" in keywords:
        suggestions.append(2)
    if "canary wharf" in keywords or "professional" in keywords:
        suggestions.append(3)
    
    return suggestions[:3]

def extract_preferences(message: str) -> dict:
    """Extract user preferences from message"""
    preferences = {}
    message_lower = message.lower()
    
    # Extract budget
    if "£" in message or "pound" in message_lower:
        # Simple extraction - in production use NLP
        import re
        numbers = re.findall(r'£?(\d+)k', message_lower)
        if numbers:
            preferences["budget"] = int(numbers[0]) * 1000
    
    # Extract bedrooms
    bedroom_match = re.search(r'(\d+)[- ]bed', message_lower)
    if bedroom_match:
        preferences["bedrooms"] = int(bedroom_match.group(1))
    
    # Extract location
    locations = ["shoreditch", "camden", "canary wharf", "richmond", "notting hill"]
    for loc in locations:
        if loc in message_lower:
            preferences["location"] = loc.title()
            break
    
    return preferences if preferences else None