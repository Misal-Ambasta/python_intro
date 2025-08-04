# zomato_v1: Basic SQLAlchemy imports for restaurant CRUD
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
# zomato_v2: Relationship loading import for efficient queries
from sqlalchemy.orm import selectinload
from sqlalchemy import and_, func
from models import Restaurant, MenuItem
from schemas import RestaurantCreate, RestaurantUpdate, MenuItemCreate, MenuItemUpdate
from typing import List, Optional
# zomato_v2: Decimal import for price calculations
from decimal import Decimal

# zomato_v1: Restaurant CRUD operations as per V1 requirements
async def create_restaurant(db: AsyncSession, restaurant: RestaurantCreate) -> Restaurant:
    """Create a new restaurant"""
    db_restaurant = Restaurant(**restaurant.dict())
    db.add(db_restaurant)
    await db.commit()
    await db.refresh(db_restaurant)
    return db_restaurant

# zomato_v1: Get restaurant by ID
async def get_restaurant(db: AsyncSession, restaurant_id: int) -> Optional[Restaurant]:
    """Get a restaurant by ID"""
    result = await db.execute(select(Restaurant).filter(Restaurant.id == restaurant_id))
    return result.scalars().first()

# zomato_v1: Get restaurant by name (for duplicate checking)
async def get_restaurant_by_name(db: AsyncSession, name: str) -> Optional[Restaurant]:
    """Get a restaurant by name"""
    result = await db.execute(select(Restaurant).filter(Restaurant.name == name))
    return result.scalars().first()

# zomato_v1: Get all restaurants with pagination
async def get_restaurants(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Restaurant]:
    """Get all restaurants with pagination"""
    result = await db.execute(select(Restaurant).offset(skip).limit(limit))
    return result.scalars().all()

# zomato_v1: Get active restaurants only
async def get_active_restaurants(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Restaurant]:
    """Get only active restaurants with pagination"""
    result = await db.execute(
        select(Restaurant)
        .filter(Restaurant.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

# zomato_v1: Search restaurants by cuisine type
async def search_restaurants_by_cuisine(db: AsyncSession, cuisine_type: str, skip: int = 0, limit: int = 100) -> List[Restaurant]:
    """Search restaurants by cuisine type"""
    result = await db.execute(
        select(Restaurant)
        .filter(Restaurant.cuisine_type.ilike(f"%{cuisine_type}%"))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

# zomato_v2: Get restaurant with menu items (relationship loading)
async def get_restaurant_with_menu(db: AsyncSession, restaurant_id: int) -> Optional[Restaurant]:
    """Get a restaurant with all its menu items"""
    result = await db.execute(
        select(Restaurant)
        .options(selectinload(Restaurant.menu_items))
        .filter(Restaurant.id == restaurant_id)
    )
    return result.scalars().first()

# zomato_v1: Update restaurant
async def update_restaurant(db: AsyncSession, restaurant_id: int, restaurant_update: RestaurantUpdate) -> Optional[Restaurant]:
    """Update a restaurant"""
    result = await db.execute(select(Restaurant).filter(Restaurant.id == restaurant_id))
    db_restaurant = result.scalars().first()
    
    if db_restaurant:
        update_data = restaurant_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_restaurant, field, value)
        
        await db.commit()
        await db.refresh(db_restaurant)
    
    return db_restaurant

# zomato_v1: Delete restaurant
async def delete_restaurant(db: AsyncSession, restaurant_id: int) -> bool:
    """Delete a restaurant"""
    result = await db.execute(select(Restaurant).filter(Restaurant.id == restaurant_id))
    db_restaurant = result.scalars().first()
    
    if db_restaurant:
        await db.delete(db_restaurant)
        await db.commit()
        return True
    
    return False

# zomato_v2: Menu Item CRUD operations for menu management
async def create_menu_item(db: AsyncSession, menu_item: MenuItemCreate, restaurant_id: int) -> MenuItem:
    """Create a new menu item for a restaurant"""
    db_menu_item = MenuItem(**menu_item.dict(), restaurant_id=restaurant_id)
    db.add(db_menu_item)
    await db.commit()
    await db.refresh(db_menu_item)
    return db_menu_item

# zomato_v2: Get menu item by ID
async def get_menu_item(db: AsyncSession, item_id: int) -> Optional[MenuItem]:
    """Get a menu item by ID"""
    result = await db.execute(select(MenuItem).filter(MenuItem.id == item_id))
    return result.scalars().first()

# zomato_v2: Get menu item with restaurant details
async def get_menu_item_with_restaurant(db: AsyncSession, item_id: int) -> Optional[MenuItem]:
    """Get a menu item with restaurant details"""
    result = await db.execute(
        select(MenuItem)
        .options(selectinload(MenuItem.restaurant))
        .filter(MenuItem.id == item_id)
    )
    return result.scalars().first()

# zomato_v2: Get all menu items
async def get_menu_items(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[MenuItem]:
    """Get all menu items with pagination"""
    result = await db.execute(select(MenuItem).offset(skip).limit(limit))
    return result.scalars().all()

# zomato_v2: Get menu items for specific restaurant
async def get_restaurant_menu(db: AsyncSession, restaurant_id: int, skip: int = 0, limit: int = 100) -> List[MenuItem]:
    """Get all menu items for a specific restaurant"""
    result = await db.execute(
        select(MenuItem)
        .filter(MenuItem.restaurant_id == restaurant_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

# zomato_v2: Advanced menu item search with filters
async def search_menu_items(
    db: AsyncSession, 
    category: Optional[str] = None, 
    vegetarian: Optional[bool] = None,
    vegan: Optional[bool] = None,
    available: Optional[bool] = None,
    skip: int = 0, 
    limit: int = 100
) -> List[MenuItem]:
    """Search menu items by various filters"""
    query = select(MenuItem)
    
    filters = []
    if category:
        filters.append(MenuItem.category.ilike(f"%{category}%"))
    if vegetarian is not None:
        filters.append(MenuItem.is_vegetarian == vegetarian)
    if vegan is not None:
        filters.append(MenuItem.is_vegan == vegan)
    if available is not None:
        filters.append(MenuItem.is_available == available)
    
    if filters:
        query = query.filter(and_(*filters))
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# zomato_v2: Update menu item
async def update_menu_item(db: AsyncSession, item_id: int, menu_item_update: MenuItemUpdate) -> Optional[MenuItem]:
    """Update a menu item"""
    result = await db.execute(select(MenuItem).filter(MenuItem.id == item_id))
    db_menu_item = result.scalars().first()
    
    if db_menu_item:
        update_data = menu_item_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_menu_item, field, value)
        
        await db.commit()
        await db.refresh(db_menu_item)
    
    return db_menu_item

# zomato_v2: Delete menu item
async def delete_menu_item(db: AsyncSession, item_id: int) -> bool:
    """Delete a menu item"""
    result = await db.execute(select(MenuItem).filter(MenuItem.id == item_id))
    db_menu_item = result.scalars().first()
    
    if db_menu_item:
        await db.delete(db_menu_item)
        await db.commit()
        return True
    
    return False

# zomato_v2: Calculate average menu price per restaurant
async def get_restaurant_average_price(db: AsyncSession, restaurant_id: int) -> Optional[Decimal]:
    """Calculate average menu price for a restaurant"""
    result = await db.execute(
        select(func.avg(MenuItem.price))
        .filter(MenuItem.restaurant_id == restaurant_id)
    )
    avg_price = result.scalar()
    return Decimal(str(avg_price)).quantize(Decimal('0.01')) if avg_price else None