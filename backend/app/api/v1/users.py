from fastapi import APIRouter, HTTPException
from app.schemas.user import User, UserCreate, UserPreferences, SavedProperty
from typing import List
from datetime import datetime

router = APIRouter()

# Mock user database
MOCK_USERS = {
    1: {
        "id": 1,
        "email": "john.doe@example.com",
        "full_name": "John Doe",
        "phone": "+44 20 1234 5678",
        "is_active": True,
        "preferences": {
            "preferred_locations": ["Shoreditch", "Camden"],
            "min_price": 300000,
            "max_price": 600000,
            "preferred_bedrooms": 2,
            "preferred_property_types": ["Apartment", "Flat"],
            "must_have_features": ["Parking", "Balcony"]
        },
        "created_at": "2024-01-10T10:00:00Z"
    }
}

SAVED_PROPERTIES = {
    1: [  # user_id: [property_ids]
        {"property_id": 1, "saved_at": "2024-01-15T14:30:00Z"},
        {"property_id": 3, "saved_at": "2024-01-16T09:15:00Z"}
    ]
}

@router.post("/register", response_model=User)
async def register_user(user: UserCreate):
    """Register a new user"""
    # Check if email exists
    for existing_user in MOCK_USERS.values():
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create new user
    new_id = max(MOCK_USERS.keys()) + 1 if MOCK_USERS else 1
    new_user = {
        "id": new_id,
        "email": user.email,
        "full_name": user.full_name,
        "phone": user.phone,
        "is_active": True,
        "preferences": None,
        "created_at": datetime.now().isoformat()
    }
    
    MOCK_USERS[new_id] = new_user
    return new_user

@router.get("/{user_id}", response_model=User)
async def get_user(user_id: int):
    """Get user by ID"""
    if user_id not in MOCK_USERS:
        raise HTTPException(status_code=404, detail="User not found")
    
    return MOCK_USERS[user_id]

@router.put("/{user_id}/preferences")
async def update_preferences(user_id: int, preferences: UserPreferences):
    """Update user preferences"""
    if user_id not in MOCK_USERS:
        raise HTTPException(status_code=404, detail="User not found")
    
    MOCK_USERS[user_id]["preferences"] = preferences.dict()
    return {"message": "Preferences updated", "preferences": preferences}

@router.get("/{user_id}/preferences", response_model=UserPreferences)
async def get_preferences(user_id: int):
    """Get user preferences"""
    if user_id not in MOCK_USERS:
        raise HTTPException(status_code=404, detail="User not found")
    
    prefs = MOCK_USERS[user_id].get("preferences")
    if not prefs:
        raise HTTPException(status_code=404, detail="No preferences set")
    
    return prefs

@router.post("/{user_id}/saved-properties/{property_id}")
async def save_property(user_id: int, property_id: int):
    """Save a property to user's favorites"""
    if user_id not in MOCK_USERS:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_id not in SAVED_PROPERTIES:
        SAVED_PROPERTIES[user_id] = []
    
    # Check if already saved
    for saved in SAVED_PROPERTIES[user_id]:
        if saved["property_id"] == property_id:
            raise HTTPException(status_code=400, detail="Property already saved")
    
    SAVED_PROPERTIES[user_id].append({
        "property_id": property_id,
        "saved_at": datetime.now().isoformat()
    })
    
    return {"message": "Property saved successfully"}

@router.delete("/{user_id}/saved-properties/{property_id}")
async def unsave_property(user_id: int, property_id: int):
    """Remove a property from user's favorites"""
    if user_id not in MOCK_USERS:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_id not in SAVED_PROPERTIES:
        raise HTTPException(status_code=404, detail="No saved properties")
    
    SAVED_PROPERTIES[user_id] = [
        p for p in SAVED_PROPERTIES[user_id] 
        if p["property_id"] != property_id
    ]
    
    return {"message": "Property removed from saved"}

@router.get("/{user_id}/saved-properties", response_model=List[SavedProperty])
async def get_saved_properties(user_id: int):
    """Get all saved properties for a user"""
    if user_id not in MOCK_USERS:
        raise HTTPException(status_code=404, detail="User not found")
    
    return SAVED_PROPERTIES.get(user_id, [])

@router.get("/{user_id}/recommendations")
async def get_user_recommendations(user_id: int):
    """Get personalized property recommendations based on user preferences"""
    if user_id not in MOCK_USERS:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = MOCK_USERS[user_id]
    prefs = user.get("preferences")
    
    if not prefs:
        return {
            "message": "Set your preferences to get personalized recommendations",
            "recommended_properties": []
        }
    
    # Simple recommendation logic based on preferences
    recommended_ids = []
    
    if "Shoreditch" in prefs.get("preferred_locations", []):
        recommended_ids.append(1)
    if "Camden" in prefs.get("preferred_locations", []):
        recommended_ids.append(2)
    if prefs.get("preferred_bedrooms") == 1:
        recommended_ids.append(3)
    
    return {
        "message": "Recommendations based on your preferences",
        "recommended_properties": recommended_ids,
        "based_on": {
            "locations": prefs.get("preferred_locations", []),
            "budget": f"£{prefs.get('min_price', 0)} - £{prefs.get('max_price', 0)}",
            "bedrooms": prefs.get("preferred_bedrooms")
        }
    }