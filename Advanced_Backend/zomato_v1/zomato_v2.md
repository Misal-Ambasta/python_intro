## Q: 2  
### Version 2: Restaurant-Menu System with Relationships  
**Intermediate Level – One-to-Many Relationships**

---

### 📝 Problem Statement
Extend your restaurant system to include **menu management**. Restaurants can now have **multiple menu items**, creating a proper restaurant–menu relationship similar to the user–posts example in your curriculum.

---

### ✅ Requirements

#### New Features (In addition to Version 1):
- Menu item management for each restaurant  
- Relationship between restaurants and their menu items  
- Advanced querying with relationships  

---

### 🍽️ Menu Item Model should include:
- `id` (Primary Key)  
- `name` (Required, 3–100 characters)  
- `description` (Optional)  
- `price` (Required, Decimal with 2 decimal places)  
- `category` (Required, e.g., `"Appetizer"`, `"Main Course"`, `"Dessert"`, `"Beverage"`)  
- `is_vegetarian` (Boolean, default `False`)  
- `is_vegan` (Boolean, default `False`)  
- `is_available` (Boolean, default `True`)  
- `preparation_time` (Integer, minutes)  
- `restaurant_id` (Foreign Key to Restaurant)  
- `created_at` (Timestamp)  
- `updated_at` (Timestamp)  

---

### 📡 Additional API Endpoints

- `POST /restaurants/{restaurant_id}/menu-items/` – Add menu item to restaurant  
- `GET /menu-items/` – List all menu items  
- `GET /menu-items/{item_id}` – Get specific menu item  
- `GET /menu-items/{item_id}/with-restaurant` – Get menu item with restaurant details  
- `GET /restaurants/{restaurant_id}/menu` – Get all menu items for a restaurant  
- `GET /restaurants/{restaurant_id}/with-menu` – Get restaurant with all menu items  
- `PUT /menu-items/{item_id}` – Update menu item  
- `DELETE /menu-items/{item_id}` – Delete menu item  
- `GET /menu-items/search?category={category}&vegetarian={bool}` – Search menu items  

---

### ✨ Enhanced Features

- Filter menu items by dietary preferences (vegetarian/vegan)  
- Search menu items by category  
- Calculate average menu price per restaurant  
- Get restaurants with their complete menu  

---

### 🛠️ Technical Requirements

- Implement proper SQLAlchemy relationships (One restaurant → Many menu items)  
- Use `selectinload` for efficient relationship loading  
- Create nested Pydantic schemas for complex responses  
- Cascade delete (when restaurant is deleted, remove all its menu items)  
- Add price validation (must be positive)  


## Directory Structure:
zomato_v2/
    |— main. py
    |— database. py
    |— models. py
    |—schemas. py
    |—crud. py
    |—routes/
        |— __init__.py
        |— restaurants. py
        |— menu_items. py   
    |— requirements. txt
    |— README.md
