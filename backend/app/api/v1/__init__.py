from fastapi import APIRouter
from app.api.v1 import properties, chat, analytics, users

# Create main v1 router
api_router = APIRouter()

# Include all sub-routers
api_router.include_router(properties.router, prefix="/properties", tags=["Properties"])
api_router.include_router(chat.router, prefix="/chat", tags=["Chat"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])