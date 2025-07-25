import re
from datetime import datetime
from collections import defaultdict

class Employee:
    company_name = "GlobalTech Solutions"
    total_employees = 0
    departments = defaultdict(int)
    tax_rates = {'USA': 0.25, 'India': 0.18, 'UK': 0.25}
    next_employee_id = 1
    approved_departments = ['Engineering', 'HR', 'Finance', 'Marketing', 'Sales', 'Support']

    def __init__(self, name, department, base_salary, country, email, hire_date=None):
        if not Employee.is_valid_department(department):
            raise ValueError(f"{department} is not a valid department.")
        
        self.employee_id = Employee.generate_employee_id()
        self.name = name
        self.department = department
        self.base_salary = float(base_salary)
        self.country = country
        self.email = email
        self.hire_date = hire_date or datetime.now().date()
        self.performance_ratings = []

        # Update class-level data
        Employee.total_employees += 1
        Employee.departments[department] += 1

    # ---------------------
    # Static Methods
    # ---------------------
    @staticmethod
    def validate_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def calculate_tax(salary, country):
        rate = Employee.tax_rates.get(country, 0.2)
        return round(salary * rate, 2)

    @staticmethod
    def is_valid_department(dept):
        return dept in Employee.approved_departments

    @staticmethod
    def generate_employee_id():
        year = datetime.now().year
        eid = f"EMP-{year}-{Employee.next_employee_id:04d}"
        Employee.next_employee_id += 1
        return eid

    # ---------------------
    # Class Methods
    # ---------------------
    @classmethod
    def from_csv_data(cls, csv_line):
        try:
            name, dept, salary, country, email = csv_line.strip().split(',')
            if not cls.validate_email(email):
                raise ValueError("Invalid email format.")
            return cls(name, dept, float(salary), country, email)
        except Exception as e:
            raise ValueError(f"Error parsing CSV data: {e}")

    @classmethod
    def get_department_stats(cls):
        return {
            "total_departments": len(cls.departments),
            "departments": dict(cls.departments),
            "total_employees": cls.total_employees
        }

    @classmethod
    def set_tax_rate(cls, country, rate):
        if not (0 <= rate <= 1):
            raise ValueError("Tax rate must be between 0 and 1.")
        cls.tax_rates[country] = rate

    @classmethod
    def hire_bulk_employees(cls, employee_list):
        hired = []
        for data in employee_list:
            try:
                emp = cls.from_csv_data(data)
                hired.append(emp)
            except Exception as e:
                print(f"Failed to hire from data '{data}': {e}")
        return hired

    # ---------------------
    # Instance Methods
    # ---------------------
    def add_performance_rating(self, rating):
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5.")
        self.performance_ratings.append(rating)

    def get_average_performance(self):
        if not self.performance_ratings:
            return 0.0
        return round(sum(self.performance_ratings) / len(self.performance_ratings), 2)

    def calculate_net_salary(self):
        tax = Employee.calculate_tax(self.base_salary, self.country)
        return round(self.base_salary - tax, 2)

    def get_years_of_service(self):
        today = datetime.now().date()
        return (today - self.hire_date).days // 365

    def is_eligible_for_bonus(self):
        return self.get_average_performance() > 3.5 and self.get_years_of_service() > 1
