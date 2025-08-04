# Zomato V2 - Restaurant-Menu Management System

A comprehensive restaurant management system with menu functionality, built with FastAPI and SQLAlchemy. This project demonstrates progressive development from V1 (basic restaurant management) to V2 (restaurant-menu relationships).

## 🚀 Features

### Version 2 Features (New)
- **Menu Item Management**: Full CRUD operations for menu items
- **Restaurant-Menu Relationships**: One-to-many relationship between restaurants and menu items
- **Advanced Filtering**: Search menu items by category, dietary preferences, and availability
- **Relationship Loading**: Efficient loading of related data using `selectinload`
- **Cascade Operations**: Automatic deletion of menu items when restaurant is deleted
- **Price Calculations**: Average menu price calculation per restaurant
- **Dietary Preferences**: Vegetarian and vegan filtering options

### Version 1 Features (Foundation)
- Restaurant CRUD operations
- Restaurant search by cuisine
- Active/inactive restaurant filtering
- Data validation and error handling
- Async database operations
- Phone number and time validation

## 📡 API Endpoints

### Restaurant Endpoints (V1 + V2)
- `POST /restaurants/` - Create a new restaurant
- `GET /restaurants/` - List all restaurants (with pagination)
- `GET /restaurants/active` - List active restaurants only
- `GET /restaurants/search?cuisine={cuisine}` - Search restaurants by cuisine
- `GET /restaurants/{restaurant_id}` - Get specific restaurant
- `GET /restaurants/{restaurant_id}/with-menu` - Get restaurant with all menu items *(V2)*
- `PUT /restaurants/{restaurant_id}` - Update restaurant
- `DELETE /restaurants/{restaurant_id}` - Delete restaurant (cascades to menu items)

### Menu Item Endpoints (V2)
- `POST /restaurants/{restaurant_id}/menu-items/` - Add menu item to restaurant
- `GET /menu-items/` - List all menu items
- `GET /menu-items/{item_id}` - Get specific menu item
- `GET /menu-items/{item_id}/with-restaurant` - Get menu item with restaurant details
- `GET /restaurants/{restaurant_id}/menu` - Get all menu items for a restaurant
- `GET /menu-items/search` - Search menu items with filters:
  - `category` - Filter by category (Appetizer, Main Course, Dessert, Beverage)
  - `vegetarian` - Filter by vegetarian status
  - `vegan` - Filter by vegan status
  - `available` - Filter by availability
- `PUT /menu-items/{item_id}` - Update menu item
- `DELETE /menu-items/{item_id}` - Delete menu item
- `GET /restaurants/{restaurant_id}/average-price` - Get average menu price

## 🗄️ Data Models

### Restaurant Model (V1)
- `id` (Primary Key)
- `name` (Required, unique, 3-100 characters)
- `description` (Optional)
- `cuisine_type` (Required, 1-50 characters)
- `address` (Required, 1-255 characters)
- `phone_number` (Required, 10-20 characters with validation)
- `rating` (0.0-5.0, default 0.0)
- `is_active` (Boolean, default True)
- `opening_time` (Required, HH:MM:SS format)
- `closing_time` (Required, HH:MM:SS format, must be after opening_time)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

### Menu Item Model (V2)
- `id` (Primary Key)
- `name` (Required, 3-100 characters)
- `description` (Optional)
- `price` (Required, Decimal with 2 decimal places, must be positive)
- `category` (Required, e.g., "Appetizer", "Main Course", "Dessert", "Beverage")
- `is_vegetarian` (Boolean, default False)
- `is_vegan` (Boolean, default False)
- `is_available` (Boolean, default True)
- `preparation_time` (Integer, minutes)
- `restaurant_id` (Foreign Key to Restaurant)
- `created_at` (Timestamp)
- `updated_at` (Timestamp)

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Steps

1. **Clone/Download the Project**:
   ```bash
   cd zomato_v1
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv .venv
   ```

3. **Activate Virtual Environment**:
   ```bash
   # Windows
   source .venv/Scripts/activate
   
   # Linux/Mac
   source .venv/bin/activate
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application**:
   ```bash
   python main.py
   ```

6. **Access the API**:
   - **API Documentation**: http://localhost:8000/docs
   - **Alternative Docs**: http://localhost:8000/redoc
   - **Health Check**: http://localhost:8000/health
   - **Root Endpoint**: http://localhost:8000/

## 📁 Project Structure

```
zomato_v1/
├── main.py                 # FastAPI application entry point
├── database.py            # Database configuration and connection
├── models.py              # SQLAlchemy models (Restaurant, MenuItem)
├── schemas.py             # Pydantic schemas for validation
├── crud.py                # Database operations (CRUD functions)
├── routes/
│   ├── __init__.py        # Router package initialization
│   ├── restaurants.py     # Restaurant endpoints (V1 + V2)
│   └── menu_items.py      # Menu item endpoints (V2)
├── requirements.txt       # Python dependencies
├── restaurants.db         # SQLite database file (auto-created)
├── .gitignore            # Git ignore file
├── README.md             # This documentation
├── IMPLEMENTATION_SUMMARY.md  # V1 vs V2 feature breakdown
├── zomato_v1.md          # V1 requirements
└── zomato_v2.md          # V2 requirements
```

## ⚡ Technical Features

- **Async/Await**: Full async support for database operations
- **SQLAlchemy 2.0**: Modern SQLAlchemy with async support and relationships
- **Pydantic V2**: Data validation and serialization with custom validators
- **Relationship Loading**: Efficient `selectinload` for related data
- **Cascade Delete**: Automatic cleanup of related records
- **Input Validation**: Comprehensive validation for all inputs
- **Error Handling**: Proper HTTP status codes and error messages
- **Pagination**: Built-in pagination for list endpoints
- **Search & Filter**: Advanced filtering capabilities
- **Functional Programming**: Pure functions and immutable patterns where possible

## 📝 Usage Examples

### Create a Restaurant
```bash
curl -X POST "http://localhost:8000/restaurants/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Pizza Palace",
    "description": "Authentic Italian cuisine",
    "cuisine_type": "Italian",
    "address": "123 Main St, Downtown",
    "phone_number": "+1234567890",
    "opening_time": "10:00:00",
    "closing_time": "22:00:00"
  }'
```

### Add Menu Item to Restaurant
```bash
curl -X POST "http://localhost:8000/restaurants/1/menu-items/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Margherita Pizza",
    "description": "Classic pizza with tomato sauce, mozzarella, and fresh basil",
    "price": 12.99,
    "category": "Main Course",
    "is_vegetarian": true,
    "is_vegan": false,
    "preparation_time": 15
  }'
```

### Search Menu Items by Filters
```bash
# Search vegetarian main courses
curl "http://localhost:8000/menu-items/search?category=Main%20Course&vegetarian=true"

# Search available vegan items
curl "http://localhost:8000/menu-items/search?vegan=true&available=true"
```

### Get Restaurant with Menu
```bash
curl "http://localhost:8000/restaurants/1/with-menu"
```

### Calculate Average Menu Price
```bash
curl "http://localhost:8000/restaurants/1/average-price"
```

## 🧪 Testing the API

1. **Start the server**: `python main.py`
2. **Open browser**: Navigate to http://localhost:8000/docs
3. **Interactive testing**: Use the Swagger UI to test all endpoints
4. **Sample data**: Create a restaurant first, then add menu items to it

## 🔧 Development Guidelines

- **Functional Programming**: Uses pure functions and avoids side effects where possible
- **Async Patterns**: All database operations are asynchronous
- **Type Hints**: Full type annotations throughout the codebase
- **Error Handling**: Comprehensive error handling with meaningful messages
- **Code Organization**: Clear separation of concerns across modules
- **Documentation**: Inline comments distinguish V1 vs V2 components

## 📊 Database Schema

The application uses SQLite with the following relationships:
- **One-to-Many**: Restaurant → Menu Items
- **Foreign Key**: menu_items.restaurant_id → restaurants.id
- **Cascade Delete**: Deleting a restaurant removes all its menu items

## 🚦 Version History

- **V2.0.0** (Current): Added menu management, relationships, advanced filtering, and dietary preferences
- **V1.0.0**: Basic restaurant CRUD operations with validation and search

## 🤝 Contributing

This project follows functional programming principles and modern Python async patterns. When contributing:
1. Maintain async/await patterns
2. Use pure functions where possible
3. Add proper type hints
4. Include comprehensive error handling
5. Update tests and documentation

## 📄 License

This project is for educational purposes as part of the Advanced Backend Development curriculum.