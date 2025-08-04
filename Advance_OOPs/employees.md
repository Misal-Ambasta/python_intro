# Q: 2 - Employee Management System with Class Variables and Methods

## Problem Statement
Create an Employee class for a multinational company with department tracking and payroll calculations.

## Requirements

### Class Variables:
- `company_name`
- `total_employees`
- `departments` (dict tracking employee count per dept)
- `tax_rates` (dict by country)
- `next_employee_id`

### Instance Variables:
- `employee_id`
- `name`
- `department`
- `base_salary`
- `country`
- `hire_date`
- `performance_ratings` (list)

### Static Methods:

#### `validate_email(email)`:
- Check proper email format with domain validation

#### `calculate_tax(salary, country)`:
- Calculate tax based on country rates

#### `is_valid_department(dept)`:
- Check against approved departments list

#### `generate_employee_id()`:
- Create unique ID with format "EMP-YYYY-XXXX"

### Class Methods:

#### `from_csv_data(csv_line)`:
- Create employee from "name,dept,salary,country,email" format

#### `get_department_stats()`:
- Return detailed department statistics

#### `set_tax_rate(country, rate)`:
- Update tax rate for specific country

#### `hire_bulk_employees(employee_list)`:
- Process multiple hires at once

### Instance Methods:

#### `add_performance_rating(rating)`:
- Add rating (1-5 scale) with validation

#### `get_average_performance()`:
- Calculate average of all ratings

#### `calculate_net_salary()`:
- Base salary minus taxes

#### `get_years_of_service()`:
- Calculate from hire date to current date

#### `is_eligible_for_bonus()`:
- Check if avg performance > 3.5 and service > 1 year