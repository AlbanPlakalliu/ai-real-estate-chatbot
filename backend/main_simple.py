from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import math
import uuid


app = FastAPI(title="London Homes AI API", version="1.0.0")

# ========== SCHEMAS ==========
class Property(BaseModel):
    id: int
    title: str
    description: str
    price: float
    bedrooms: int
    bathrooms: int
    area: Optional[float] = None
    address: str
    city: str
    postcode: Optional[str] = None
    property_type: str
    image_urls: List[str]
    features: List[str]
    is_available: bool
    views: int
    created_at: str
    updated_at: str

class PropertySearch(BaseModel):
    location: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

# ========== DATA ==========
PROPERTIES = [
    {
        "id": 1, "title": "Modern 2-Bed Apartment in Shoreditch",
        "description": "Stunning apartment with city views", "price": 450000,
        "bedrooms": 2, "bathrooms": 1, "area": 75.0, "address": "123 Brick Lane",
        "city": "London", "postcode": "E1 6QL", "property_type": "Apartment",
        "image_urls": ["https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800"],
        "features": ["Parking", "Balcony", "Gym"], "is_available": True, "views": 245,
        "created_at": "2024-01-15T10:00:00Z", "updated_at": "2024-01-18T14:30:00Z"
    },
    {
        "id": 2, "title": "Luxury 3-Bed House in Camden",
        "description": "Beautiful Victorian house with garden", "price": 750000,
        "bedrooms": 3, "bathrooms": 2, "area": 120.0, "address": "45 Parkway",
        "city": "London", "postcode": "NW1 7PN", "property_type": "House",
        "image_urls": ["https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800"],
        "features": ["Garden", "Parking"], "is_available": True, "views": 387,
        "created_at": "2024-01-10T09:00:00Z", "updated_at": "2024-01-18T16:00:00Z"
    },
    {
        "id": 3, "title": "Stylish 1-Bed Flat in Canary Wharf",
        "description": "Modern flat with Thames views", "price": 380000,
        "bedrooms": 1, "bathrooms": 1, "area": 50.0, "address": "Canary Wharf Tower",
        "city": "London", "postcode": "E14 5AB", "property_type": "Flat",
        "image_urls": ["https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800"],
        "features": ["Concierge", "Gym", "Pool"], "is_available": True, "views": 156,
        "created_at": "2024-01-12T11:00:00Z", "updated_at": "2024-01-18T10:15:00Z"
    },
    {
        "id": 4, "title": "Spacious 4-Bed Family Home in Richmond",
        "description": "Perfect family home near Richmond Park", "price": 950000,
        "bedrooms": 4, "bathrooms": 3, "area": 180.0, "address": "78 Richmond Hill",
        "city": "London", "postcode": "TW10 6RN", "property_type": "House",
        "image_urls": ["https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800"],
        "features": ["Garden", "Parking", "Garage"], "is_available": True, "views": 423,
        "created_at": "2024-01-08T08:00:00Z", "updated_at": "2024-01-18T09:00:00Z"
    },
    {
        "id": 5, "title": "Charming 2-Bed Cottage in Notting Hill",
        "description": "Character property in desirable location", "price": 620000,
        "bedrooms": 2, "bathrooms": 1, "area": 85.0, "address": "12 Portobello Road",
        "city": "London", "postcode": "W11 2DY", "property_type": "House",
        "image_urls": ["https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800"],
        "features": ["Fireplace", "Period Features"], "is_available": True, "views": 298,
        "created_at": "2024-01-14T12:00:00Z", "updated_at": "2024-01-18T15:45:00Z"
    }
]

# ========== ENDPOINTS ==========
@app.get("/")
def root():
    return {"message": "London Homes AI API", "version": "1.0.0", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/api/v1/properties", response_model=List[Property])
def get_properties(skip: int = 0, limit: int = 10):
    """Get all properties"""
    return PROPERTIES[skip:skip+limit]

@app.get("/api/v1/properties/{property_id}", response_model=Property)
def get_property(property_id: int):
    """Get property by ID"""
    for p in PROPERTIES:
        if p["id"] == property_id:
            return p
    raise HTTPException(404, "Property not found")

@app.post("/api/v1/properties/search")
def search(search: PropertySearch):
    """Search properties"""
    filtered = PROPERTIES
    if search.location:
        filtered = [p for p in filtered if search.location.lower() in p["address"].lower()]
    if search.min_price:
        filtered = [p for p in filtered if p["price"] >= search.min_price]
    if search.max_price:
        filtered = [p for p in filtered if p["price"] <= search.max_price]
    if search.bedrooms:
        filtered = [p for p in filtered if p["bedrooms"] == search.bedrooms]
    if search.bathrooms:
        filtered = [p for p in filtered if p["bathrooms"] == search.bathrooms]
    return {"properties": filtered, "total": len(filtered)}

@app.post("/api/v1/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    """Chat endpoint - demo"""
    response_text = f"Hello! You said: '{req.message}'. I'm a demo chatbot!"
    return ChatResponse(
        response=response_text,
        conversation_id=str(uuid.uuid4())
    )

@app.get("/api/v1/analytics/stats")
def stats():
    """Get statistics"""
    return {
        "total_properties": len(PROPERTIES),
        "average_price": sum(p["price"] for p in PROPERTIES) / len(PROPERTIES),
        "most_popular_area": "East London",
        "total_users": 1247,
        "active_conversations": 89
    }

@app.get("/api/v1/analytics/popular-searches")
def popular_searches():
    """Popular search terms"""
    return {
        "searches": [
            {"term": "2 bedroom apartment", "count": 145},
            {"term": "house with garden", "count": 98},
            {"term": "central london flat", "count": 87}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main_simple:app", host="0.0.0.0", port=8000, reload=True)