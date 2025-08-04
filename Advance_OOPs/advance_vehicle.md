# Q: 3 - Advanced Vehicle Fleet Management with Inheritance

## Problem Statement
Create a comprehensive vehicle management system for a rental company.

## Base Class: Vehicle

### Attributes:
- `vehicle_id`
- `make`
- `model`
- `year`
- `daily_rate`
- `is_available`
- `mileage`
- `fuel_type`

### Methods:
- `rent()`
- `return_vehicle()`
- `calculate_rental_cost(days)`
- `get_vehicle_info()`

## Derived Classes:

### Car(Vehicle):
- `seating_capacity`
- `transmission_type`
- `has_gps`

### Motorcycle(Vehicle):
- `engine_cc`
- `bike_type` (sport/cruiser/touring)

### Truck(Vehicle):
- `cargo_capacity`
- `license_required`
- `max_weight`

## Additional Requirements:

- Each vehicle type has different pricing multipliers
- Override `calculate_rental_cost()` with type-specific logic
- Add maintenance tracking with inherited `MaintenanceRecord` class
- Implement fuel efficiency calculations based on vehicle type