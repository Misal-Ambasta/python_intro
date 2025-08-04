# Problem 1: Basic Food Menu Management System (Single Table)

## Problem Statement

Create a simple Food Menu Management API for a restaurant. The system should allow restaurant staff to manage their menu items and customers to view available food items.

## Requirements

### Data Model Requirements
- Create a FoodItem Pydantic model with proper validation
- Use a single dictionary as your database: `menu_db = {}`
- Each food item should have a unique ID as the dictionary key

### API Endpoints Required
- `GET /menu` - Get all menu items
- `GET /menu/{item_id}` - Get specific menu item
- `POST /menu` - Add new menu item (staff only)
- `PUT /menu/{item_id}` - Update existing menu item
- `DELETE /menu/{item_id}` - Remove menu item from menu
- `GET /menu/category/{category}` - Get items by category

## Food Item Model Specifications

```python
class FoodCategory(str, Enum):
    APPETIZER = "appetizer"
    MAIN_COURSE = "main_course"
    DESSERT = "dessert"
    BEVERAGE = "beverage"
    SALAD = "salad"

class FoodItem(BaseModel):
    # Your implementation here
    pass
```

### Required Fields
- **id**: Integer (auto-generated, primary key)
- **name**: String (3-100 characters, required)
- **description**: String (10-500 characters, required)
- **category**: FoodCategory enum (required)
- **price**: Decimal (must be positive, max 2 decimal places)
- **is_available**: Boolean (default True)
- **preparation_time**: Integer (minutes, 1-120)
- **ingredients**: List of strings (at least 1 ingredient)
- **calories**: Optional integer (if provided, must be positive)
- **is_vegetarian**: Boolean (default False)
- **is_spicy**: Boolean (default False)

### Custom Validations
- Name should not contain numbers or special characters (only letters and spaces)
- Price should be between $1.00 and $100.00
- Desserts and beverages cannot be marked as spicy
- If calories provided, vegetarian items should have calories < 800
- Preparation time for beverages should be ≤ 10 minutes

### Computed Properties
- **price_category**: Returns "Budget" (<$10), "Mid-range" ($10-25), "Premium" (>$25)
- **dietary_info**: Returns list like ["Vegetarian", "Spicy"] based on flags

## 🧪 Test Cases to Handle

1. **Valid Data**: Create a Margherita Pizza with all valid information
2. **Invalid Price**: Try to create item with price $0.50 (should fail)
3. **Invalid Category**: Try to mark a beverage as spicy (should fail)
4. **Missing Ingredients**: Try to create item with empty ingredients list
5. **Invalid Name**: Try to create item with name "Pizza123!" (should fail)

## 💡 Sample Data for Testing

```python
sample_menu_items = [
    {
        "name": "Margherita Pizza",
        "description": "Classic pizza with tomato sauce, mozzarella cheese, and fresh basil",
        "category": "main_course",
        "price": "15.99",
        "preparation_time": 20,
        "ingredients": ["pizza dough", "tomato sauce", "mozzarella", "basil", "olive oil"],
        "calories": 650,
        "is_vegetarian": True,
        "is_spicy": False
    },
    {
        "name": "Spicy Chicken Wings",
        "description": "Crispy chicken wings tossed in our signature hot sauce",
        "category": "appetizer",
        "price": "12.50",
        "preparation_time": 15,
        "ingredients": ["chicken wings", "hot sauce", "butter", "celery salt"],
        "calories": 420,
        "is_vegetarian": False,
        "is_spicy": True
    }
    # Add 3 more items
]
```