# zomato_v1: Basic FastAPI imports and setup
from fastapi import FastAPI
from database import create_tables
# zomato_v1: Restaurant router (basic restaurant management)
from routes.restaurants import router as restaurant_router
# zomato_v2: Menu items router (menu management with relationships)
from routes.menu_items import router as menu_items_router

# zomato_v2: Updated app configuration for V2 with menu management
app = FastAPI(
    title="Zomato V2 - Restaurant-Menu Management System",
    description="A restaurant listing system with menu management and relationships",
    version="2.0.0"
)

# zomato_v1: Basic startup event for database table creation
@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    await create_tables()

# zomato_v1: Include restaurant router (basic CRUD operations)
app.include_router(restaurant_router)
# zomato_v2: Include menu items router (menu management and relationships)
app.include_router(menu_items_router)

# zomato_v2: Updated root endpoint with V2 features
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Zomato V2 - Restaurant-Menu Management System",
        "version": "2.0.0",
        "features": [
            "Restaurant management",  # zomato_v1
            "Menu item management",   # zomato_v2
            "Restaurant-Menu relationships",  # zomato_v2
            "Advanced filtering and search"   # zomato_v2
        ],
        "docs": "/docs"
    }

# zomato_v1: Basic health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "version": "2.0.0"}

# zomato_v1: Basic uvicorn server setup
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)