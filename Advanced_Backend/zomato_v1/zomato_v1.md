# Q: 1 Assignment Overview

Build a progressive food delivery application similar to Zomato across three versions, where each version builds upon the previous one. You must use virtual environments and maintain proper directory structure as shown in the curriculum.

## Version 1: Basic Restaurant Management System
**Foundation Level - Single Table CRUD Operations**

### Problem Statement
Create a basic restaurant listing system where you can manage restaurant information. This is the foundation of your food delivery platform.

## Requirements

### Core Features:
- Complete CRUD operations for restaurants
- Restaurant data validation and error handling
- Proper API documentation with FastAPI

### Restaurant Model should include:
- **id** (Primary Key)
- **name** (Required, 3-100 characters)
- **description** (Optional text)
- **cuisine_type** (Required, e.g., "Italian", "Chinese", "Indian")
- **address** (Required)
- **phone_number** (Required, with validation)
- **rating** (Float, 0.0-5.0, default 0.0)
- **is_active** (Boolean, default True)
- **opening_time** (Time)
- **closing_time** (Time)
- **created_at** (Timestamp)
- **updated_at** (Timestamp)

### API Endpoints Required:
- `POST /restaurants/` - Create new restaurant
- `GET /restaurants/` - List all restaurants (with pagination)
- `GET /restaurants/{restaurant_id}` - Get specific restaurant
- `PUT /restaurants/{restaurant_id}` - Update restaurant
- `DELETE /restaurants/{restaurant_id}` - Delete restaurant
- `GET /restaurants/search?cuisine={cuisine_type}` - Search by cuisine
- `GET /restaurants/active` - List only active restaurants

### Technical Requirements:
- Use SQLite with async SQLAlchemy
- Implement proper Pydantic schemas for request/response validation
- Add query parameters for pagination (skip, limit)
- Include proper HTTP status codes
- Add input validation (phone number format, rating range, time validation)
- Implement error handling for duplicate restaurant names

## Directory Structure
zomato_v1/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── crud.py
├── routes.py
├── requirements.txt
└── README.md