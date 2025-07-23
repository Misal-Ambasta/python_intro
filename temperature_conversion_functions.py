
def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    res =  (celsius * 9/5) + 32
    print(f"{celsius}°C = {res}°F")

def fahrenheit_to_celsius(fahrenheit):
    """Convert Fahrenheit to Celsius."""
    res =  (fahrenheit - 32) * 5/9
    print(f"{fahrenheit}°F = {res}°C")

def celsius_to_kelvin(celsius):
    """Convert Celsius to Kelvin."""
    res = celsius + 273.15
    print(f"{celsius}°C = {res}K")

def kelvin_to_celsius(kelvin):
    """Convert Kelvin to Celsius."""
    res = round(kelvin - 273.15, 2)
    print(f"{kelvin}K = {res}°C")

celsius_to_fahrenheit(0)
fahrenheit_to_celsius(32)
kelvin_to_celsius(300)