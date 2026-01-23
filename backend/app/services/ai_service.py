import os
from typing import List, Dict

class AIService:
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.use_mock = not self.groq_key
        
        if self.use_mock:
            print("⚠️  WARNING: Running in MOCK mode (no API key found)")
        else:
            try:
                from groq import Groq
                self.client = Groq(api_key=self.groq_key)
                self.model = "llama-3.3-70b-versatile"
                print(f"✅ Connected to Groq API with model: {self.model}")
            except Exception as e:
                print(f"⚠️  Error connecting to Groq: {e}")
                self.use_mock = True
        
        self.system_prompt = """You are a helpful AI assistant for London Homes, a real estate company in London. 

Your role is to:
1. Help users find properties in London
2. Answer questions about the London real estate market
3. Provide information about neighborhoods, prices, and property features
4. Be friendly, professional, and knowledgeable

Always be helpful and accurate. If you don't know something, admit it politely."""

    def chat(self, user_message: str, conversation_history: List[Dict] = None) -> str:
        """Send a message and get a response"""
        try:
            if self.use_mock:
                return self._mock_response(user_message)
            
            # Build messages for Groq
            messages = [{"role": "system", "content": self.system_prompt}]
            
            if conversation_history:
                for msg in conversation_history:
                    messages.append({
                        "role": msg.get("role"),
                        "content": msg.get("content")
                    })
            
            messages.append({"role": "user", "content": user_message})
            
            # Call Groq API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1024,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error in AI Service: {str(e)}")
            return f"Sorry, I encountered an error: {str(e)}"
    
    def _mock_response(self, user_message: str) -> str:
        """Mock responses for testing"""
        message_lower = user_message.lower()
        
        if any(word in message_lower for word in ["property", "house", "apartment", "flat"]):
            return """I'd be happy to help you find properties in London! 

Currently, we have several properties available:
- 2-bedroom apartments in Shoreditch starting from £450,000
- 3-bedroom houses in Camden from £650,000
- Modern flats in Canary Wharf from £380,000

What type of property are you looking for? What's your budget range?"""
        
        elif any(word in message_lower for word in ["hello", "hi", "hey"]):
            return "Hello! Welcome to London Homes. How can I help you find your perfect property today?"
        
        else:
            return f"""Thank you for your message!

I'm here to help you with:
✅ Finding properties in London
✅ Information about neighborhoods
✅ Property prices and market trends

What would you like to know about London real estate?"""

# Create singleton
ai_service = AIService()