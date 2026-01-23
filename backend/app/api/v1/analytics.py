from fastapi import APIRouter
from datetime import datetime, timedelta
import random

router = APIRouter()

@router.get("/stats")
async def get_general_stats():
    """Get general platform statistics"""
    return {
        "total_properties": 5,
        "active_properties": 5,
        "total_users": 1247,
        "active_conversations": 89,
        "average_property_price": 630000,
        "total_inquiries_today": 34,
        "total_inquiries_week": 187,
        "most_popular_area": "East London",
        "properties_added_this_week": 3,
        "average_response_time_seconds": 1.2
    }

@router.get("/popular-searches")
async def get_popular_searches():
    """Get most popular search terms"""
    return {
        "time_period": "Last 7 days",
        "searches": [
            {"term": "2 bedroom apartment", "count": 145, "trend": "up"},
            {"term": "house with garden", "count": 98, "trend": "up"},
            {"term": "central london flat", "count": 87, "trend": "stable"},
            {"term": "family home richmond", "count": 76, "trend": "up"},
            {"term": "luxury apartment", "count": 54, "trend": "down"},
            {"term": "affordable studio", "count": 43, "trend": "up"}
        ]
    }

@router.get("/price-trends")
async def get_price_trends():
    """Get property price trends"""
    # Generate mock data for last 12 months
    months = []
    base_price = 550000
    
    for i in range(12):
        date = datetime.now() - timedelta(days=30 * (11 - i))
        price = base_price + random.randint(-50000, 50000)
        months.append({
            "month": date.strftime("%B %Y"),
            "average_price": price,
            "change_percent": round((price - base_price) / base_price * 100, 2)
        })
    
    return {
        "time_period": "Last 12 months",
        "data": months,
        "overall_trend": "increasing"
    }

@router.get("/area-insights")
async def get_area_insights():
    """Get insights by area"""
    return {
        "areas": [
            {
                "name": "East London",
                "average_price": 420000,
                "total_properties": 2,
                "demand_level": "high",
                "price_trend": "increasing"
            },
            {
                "name": "North London",
                "average_price": 750000,
                "total_properties": 1,
                "demand_level": "medium",
                "price_trend": "stable"
            },
            {
                "name": "South West London",
                "average_price": 950000,
                "total_properties": 1,
                "demand_level": "high",
                "price_trend": "increasing"
            },
            {
                "name": "West London",
                "average_price": 620000,
                "total_properties": 1,
                "demand_level": "very high",
                "price_trend": "increasing"
            }
        ]
    }

@router.get("/user-activity")
async def get_user_activity():
    """Get user activity statistics"""
    return {
        "daily_active_users": 342,
        "weekly_active_users": 1247,
        "monthly_active_users": 4821,
        "peak_hours": [
            {"hour": "09:00-10:00", "activity": 156},
            {"hour": "12:00-13:00", "activity": 189},
            {"hour": "18:00-19:00", "activity": 234},
            {"hour": "20:00-21:00", "activity": 198}
        ],
        "top_user_actions": [
            {"action": "property_view", "count": 2341},
            {"action": "search", "count": 1876},
            {"action": "chat_message", "count": 1234},
            {"action": "save_property", "count": 567}
        ]
    }