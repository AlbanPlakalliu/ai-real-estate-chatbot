from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.schemas.property import (
    Property, PropertyCreate, PropertyUpdate,
    PropertySearchRequest, PropertySearchResponse
)
import math

router = APIRouter()

# Mock database - në realitet do të vijë nga PostgreSQL
MOCK_PROPERTIES = [
    {
        "id": 1,
        "title": "Modern 2-Bed Apartment in Shoreditch",
        "description": "Stunning modern apartment with city views, open-plan living, and high-end finishes. Located in the heart of Shoreditch's vibrant tech scene.",
        "price": 450000,
        "bedrooms": 2,
        "bathrooms": 1,
        "area": 75.0,
        "address": "123 Brick Lane",
        "city": "London",
        "postcode": "E1 6QL",
        "latitude": 51.5225,
        "longitude": -0.0714,
        "property_type": "Apartment",
        "image_urls": [
            "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800",
            "https://images.unsplash.com/photo-1502672260066-6bc35f0aeac4?w=800"
        ],
        "features": ["Parking", "Balcony", "Gym", "Concierge"],
        "is_available": True,
        "views": 245,
        "created_at": "2024-01-15T10:00:00Z",
        "updated_at": "2024-01-18T14:30:00Z"
    },
    {
        "id": 2,
        "title": "Luxury 3-Bed Victorian House in Camden",
        "description": "Beautiful Victorian house with original features, private garden, and modern kitchen. Perfect family home in sought-after location.",
        "price": 750000,
        "bedrooms": 3,
        "bathrooms": 2,
        "area": 120.0,
        "address": "45 Parkway",
        "city": "London",
        "postcode": "NW1 7PN",
        "latitude": 51.5392,
        "longitude": -0.1426,
        "property_type": "House",
        "image_urls": [
            "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=800"
        ],
        "features": ["Garden", "Parking", "Fireplace", "Period Features"],
        "is_available": True,
        "views": 387,
        "created_at": "2024-01-10T09:00:00Z",
        "updated_at": "2024-01-18T16:00:00Z"
    },
    {
        "id": 3,
        "title": "Stylish 1-Bed Flat in Canary Wharf",
        "description": "Contemporary flat with stunning Thames views, 24hr concierge, and access to premium facilities. Ideal for professionals.",
        "price": 380000,
        "bedrooms": 1,
        "bathrooms": 1,
        "area": 50.0,
        "address": "Canary Wharf Tower",
        "city": "London",
        "postcode": "E14 5AB",
        "latitude": 51.5054,
        "longitude": -0.0235,
        "property_type": "Flat",
        "image_urls": [
            "https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=800"
        ],
        "features": ["Concierge", "Gym", "Pool", "River Views"],
        "is_available": True,
        "views": 156,
        "created_at": "2024-01-12T11:00:00Z",
        "updated_at": "2024-01-18T10:15:00Z"
    },
    {
        "id": 4,
        "title": "Spacious 4-Bed Family Home in Richmond",
        "description": "Perfect family home near Richmond Park with large garden, driveway, and excellent schools nearby. Recently renovated.",
        "price": 950000,
        "bedrooms": 4,
        "bathrooms": 3,
        "area": 180.0,
        "address": "78 Richmond Hill",
        "city": "London",
        "postcode": "TW10 6RN",
        "latitude": 51.4613,
        "longitude": -0.3037,
        "property_type": "House",
        "image_urls": [
            "https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=800"
        ],
        "features": ["Garden", "Parking", "Garage", "Near Parks"],
        "is_available": True,
        "views": 423,
        "created_at": "2024-01-08T08:00:00Z",
        "updated_at": "2024-01-18T09:00:00Z"
    },
    {
        "id": 5,
        "title": "Charming 2-Bed Cottage in Notting Hill",
        "description": "Character property in desirable Notting Hill location. Features include exposed brickwork, wooden floors, and cozy fireplace.",
        "price": 620000,
        "bedrooms": 2,
        "bathrooms": 1,
        "area": 85.0,
        "address": "12 Portobello Road",
        "city": "London",
        "postcode": "W11 2DY",
        "latitude": 51.5156,
        "longitude": -0.2058,
        "property_type": "House",
        "image_urls": [
            "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=800"
        ],
        "features": ["Fireplace", "Period Features", "Near Transport"],
        "is_available": True,
        "views": 298,
        "created_at": "2024-01-14T12:00:00Z",
        "updated_at": "2024-01-18T15:45:00Z"
    }
]

@router.get("/", response_model=List[Property])
async def get_all_properties(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: str = Query("created_at", regex="^(price|created_at|views|bedrooms)$")
):
    """Get all properties with pagination"""
    sorted_properties = sorted(
        MOCK_PROPERTIES,
        key=lambda x: x.get(sort_by, 0),
        reverse=True
    )
    return sorted_properties[skip : skip + limit]

@router.get("/{property_id}", response_model=Property)
async def get_property(property_id: int):
    """Get a specific property by ID"""
    for prop in MOCK_PROPERTIES:
        if prop["id"] == property_id:
            # Increment views
            prop["views"] += 1
            return prop
    
    raise HTTPException(status_code=404, detail="Property not found")

@router.post("/search", response_model=PropertySearchResponse)
async def search_properties(search: PropertySearchRequest):
    """Advanced property search with filters and pagination"""
    filtered = MOCK_PROPERTIES.copy()
    
    # Apply filters
    if search.location:
        filtered = [p for p in filtered if 
                   search.location.lower() in p["address"].lower() or 
                   search.location.lower() in p["city"].lower() or
                   search.location.lower() in p.get("postcode", "").lower()]
    
    if search.min_price:
        filtered = [p for p in filtered if p["price"] >= search.min_price]
    
    if search.max_price:
        filtered = [p for p in filtered if p["price"] <= search.max_price]
    
    if search.bedrooms:
        filtered = [p for p in filtered if p["bedrooms"] == search.bedrooms]
    
    if search.bathrooms:
        filtered = [p for p in filtered if p["bathrooms"] == search.bathrooms]
    
    if search.property_type:
        filtered = [p for p in filtered if search.property_type.lower() in p["property_type"].lower()]
    
    if search.min_area:
        filtered = [p for p in filtered if p.get("area", 0) >= search.min_area]
    
    if search.max_area:
        filtered = [p for p in filtered if p.get("area", 0) <= search.max_area]
    
    if search.features:
        filtered = [p for p in filtered if any(f in p.get("features", []) for f in search.features)]
    
    # Sort
    reverse = search.sort_order == "desc"
    filtered.sort(key=lambda x: x.get(search.sort_by, 0), reverse=reverse)
    
    # Pagination
    total = len(filtered)
    total_pages = math.ceil(total / search.page_size)
    start = (search.page - 1) * search.page_size
    end = start + search.page_size
    paginated = filtered[start:end]
    
    return PropertySearchResponse(
        properties=paginated,
        total=total,
        page=search.page,
        page_size=search.page_size,
        total_pages=total_pages
    )

@router.get("/featured/top")
async def get_featured_properties(limit: int = Query(3, ge=1, le=10)):
    """Get top featured properties"""
    sorted_by_views = sorted(MOCK_PROPERTIES, key=lambda x: x["views"], reverse=True)
    return sorted_by_views[:limit]

@router.get("/nearby/{property_id}")
async def get_nearby_properties(property_id: int, limit: int = Query(3, ge=1, le=10)):
    """Get properties near a specific property"""
    # In real app, would use geospatial queries
    # For now, return other properties in same area
    target = next((p for p in MOCK_PROPERTIES if p["id"] == property_id), None)
    if not target:
        raise HTTPException(status_code=404, detail="Property not found")
    
    nearby = [p for p in MOCK_PROPERTIES if p["id"] != property_id]
    return nearby[:limit]