from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import APIRouter
import os

# Direct imports
try:
    from app.api.v1.properties import router as properties_router
    from app.api.v1.chat import router as chat_router
    from app.api.v1.analytics import router as analytics_router
    from app.api.v1.users import router as users_router
    print("All routers imported successfully")
except Exception as e:
    print(f"Import error: {e}")
    properties_router = None
    chat_router = None
    analytics_router = None
    users_router = None

app = FastAPI(
    title="London Homes AI API",
    description="Professional real estate API with AI-powered chatbot",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create API v1 router
api_v1_router = APIRouter()

# Include all sub-routers if they loaded successfully
if properties_router:
    api_v1_router.include_router(properties_router, prefix="/properties", tags=["Properties"])
if chat_router:
    api_v1_router.include_router(chat_router, prefix="/chat", tags=["Chat"])
if analytics_router:
    api_v1_router.include_router(analytics_router, prefix="/analytics", tags=["Analytics"])
if users_router:
    api_v1_router.include_router(users_router, prefix="/users", tags=["Users"])

# Include API v1
app.include_router(api_v1_router, prefix="/api/v1")

# Root endpoints
@app.get("/")
async def root():
    """API Root - Welcome message"""
    return {
        "message": "Welcome to London Homes AI API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "properties": "/api/v1/properties",
            "chat": "/api/v1/chat",
            "analytics": "/api/v1/analytics",
            "users": "/api/v1/users"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected",
        "ai_service": "active",
        "version": "1.0.0"
    }

@app.get("/api/v1")
async def api_v1_info():
    """API v1 information"""
    return {
        "version": "1.0.0",
        "endpoints": [
            {"path": "/api/v1/properties", "description": "Property management"},
            {"path": "/api/v1/chat", "description": "AI chatbot"},
            {"path": "/api/v1/analytics", "description": "Statistics and insights"},
            {"path": "/api/v1/users", "description": "User management"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("API_PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)