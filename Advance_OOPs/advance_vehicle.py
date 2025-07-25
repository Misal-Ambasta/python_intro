from datetime import datetime

class MaintenanceRecord:
    def __init__(self):
        self.maintenance_log = []

    def add_maintenance(self, description, date=None):
        date = date or datetime.now().date()
        self.maintenance_log.append({'description': description, 'date': date})

    def get_maintenance_history(self):
        return self.maintenance_log

class Vehicle(MaintenanceRecord):
    def __init__(self, vehicle_id, make, model, year, daily_rate, mileage, fuel_type):
        super().__init__()
        self.vehicle_id = vehicle_id
        self.make = make
        self.model = model
        self.year = year
        self.daily_rate = daily_rate
        self.is_available = True
        self.mileage = mileage
        self.fuel_type = fuel_type  # e.g., Petrol, Diesel, Electric

    def rent(self):
        if not self.is_available:
            raise Exception(f"Vehicle {self.vehicle_id} is already rented.")
        self.is_available = False

    def return_vehicle(self):
        self.is_available = True

    def calculate_rental_cost(self, days):
        return round(self.daily_rate * days, 2)

    def get_vehicle_info(self):
        return {
            'ID': self.vehicle_id,
            'Make': self.make,
            'Model': self.model,
            'Year': self.year,
            'Rate': self.daily_rate,
            'Available': self.is_available,
            'Mileage': self.mileage,
            'Fuel': self.fuel_type
        }

    def calculate_fuel_efficiency(self):
        raise NotImplementedError("Subclasses must implement fuel efficiency logic.")

# Car Class

class Car(Vehicle):
    def __init__(self, vehicle_id, make, model, year, daily_rate, mileage, fuel_type, seating_capacity, transmission_type, has_gps):
        super().__init__(vehicle_id, make, model, year, daily_rate, mileage, fuel_type)
        self.seating_capacity = seating_capacity
        self.transmission_type = transmission_type  # Manual/Automatic
        self.has_gps = has_gps

    def calculate_rental_cost(self, days):
        gps_fee = 5 if self.has_gps else 0
        return round((self.daily_rate + gps_fee) * days * 1.1, 2)  # Car multiplier: 1.1

    def calculate_fuel_efficiency(self):
        return round(15 - (self.mileage / 10000), 2)  # Sample formula



# Motorcycle Class

class Motorcycle(Vehicle):
    def __init__(self, vehicle_id, make, model, year, daily_rate, mileage, fuel_type, engine_cc, bike_type):
        super().__init__(vehicle_id, make, model, year, daily_rate, mileage, fuel_type)
        self.engine_cc = engine_cc
        self.bike_type = bike_type  # sport, cruiser, touring

    def calculate_rental_cost(self, days):
        return round(self.daily_rate * days * 0.9, 2)  # Motorcycle multiplier: 0.9

    def calculate_fuel_efficiency(self):
        return round(35 - (self.engine_cc / 100), 2)  # Sample formula



# Truck Class

class Truck(Vehicle):
    def __init__(self, vehicle_id, make, model, year, daily_rate, mileage, fuel_type, cargo_capacity, license_required, max_weight):
        super().__init__(vehicle_id, make, model, year, daily_rate, mileage, fuel_type)
        self.cargo_capacity = cargo_capacity  # in cubic meters
        self.license_required = license_required
        self.max_weight = max_weight  # in tons

    def calculate_rental_cost(self, days):
        heavy_duty_fee = 20 if self.max_weight > 10 else 0
        return round((self.daily_rate + heavy_duty_fee) * days * 1.3, 2)  # Truck multiplier: 1.3

    def calculate_fuel_efficiency(self):
        return round(8 - (self.max_weight / 10), 2)  # Sample formula



# Example Usage

if __name__ == "__main__":
    car = Car("CAR123", "Toyota", "Camry", 2022, 50, 12000, "Petrol", 5, "Automatic", True)
    bike = Motorcycle("BIKE456", "Yamaha", "R15", 2021, 25, 8000, "Petrol", 150, "sport")
    truck = Truck("TRUCK789", "Volvo", "FH16", 2020, 100, 60000, "Diesel", 30, True, 18)

    car.rent()
    print("Car rental cost for 3 days:", car.calculate_rental_cost(3))
    print("Car fuel efficiency:", car.calculate_fuel_efficiency(), "km/l")
    car.return_vehicle()

    print("\nMotorcycle Info:", bike.get_vehicle_info())
    bike.add_maintenance("Chain oiling")
    print("Bike Maintenance History:", bike.get_maintenance_history())

    print("\nTruck Rental Cost (5 days):", truck.calculate_rental_cost(5))
    print("Truck Fuel Efficiency:", truck.calculate_fuel_efficiency(), "km/l")
