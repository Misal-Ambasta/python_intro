# Enhanced University Course Management System

## Problem Statement
Extend the previous university course management system with proper HTTP status codes, comprehensive error handling, data validation using Pydantic models, and advanced features like pagination, filtering, and academic analytics.

## Enhanced Requirements

### Pydantic Models for Data Validation:
- **StudentModel**: Validate email format, GPA range (0.0-4.0), year (1-4)
- **CourseModel**: Validate course code format, credits range (1-6)
- **ProfessorModel**: Validate email, hire_date not in future
- **EnrollmentModel**: Validate grade range (A-F or 0.0-4.0)

### HTTP Status Codes Implementation:
- **200 OK**: Successful GET/PUT operations
- **201 Created**: Successful POST operations
- **204 No Content**: Successful DELETE operations
- **400 Bad Request**: Invalid data/validation errors
- **404 Not Found**: Resource doesn't exist
- **409 Conflict**: Business rule violations (duplicate enrollment, capacity exceeded)
- **422 Unprocessable Entity**: Pydantic validation failures

## Advanced Features to Implement

### 1. Data Validation & Error Handling:
```python
# Example Pydantic models structure (don't implement)
class StudentModel(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    major: str
    year: int = Field(ge=1, le=4)
    gpa: float = Field(ge=0.0, le=4.0)
```

### 2. Query Parameters & Pagination:
- `GET /students?page=1&limit=10&major=CS&year=3`
- `GET /courses?department=CS&credits=3`
- `GET /professors?department=Math&hire_year=2020`

### 3. Advanced Analytics Endpoints:
- `GET /analytics/students/gpa-distribution`
- `GET /analytics/courses/enrollment-stats`
- `GET /analytics/professors/teaching-load`
- `GET /analytics/departments/performance`

### 4. Business Rule Validations:
- Course capacity management with waiting lists
- Prerequisite checking for advanced courses
- Academic probation status based on GPA
- Semester credit hour limits per student
- Professor teaching load restrictions

### 5. Bulk Operations:
- `POST /students/bulk` # Bulk student registration
- `POST /enrollments/bulk` # Bulk course enrollment
- `PUT /enrollments/grades/bulk` # Batch grade updates

## Expected Error Response Format
```json
{
    "detail": "Specific error message",
    "error_code": "ENROLLMENT_CAPACITY_EXCEEDED",
    "field_errors": {
        "gpa": ["GPA must be between 0.0 and 4.0"],
        "email": ["Invalid email format"]
    },
    "timestamp": "2024-01-15T10:30:00Z"
}
```

## Complex Validation Requirements

### Academic Business Rules:
- Students cannot exceed 18 credit hours per semester
- Professors cannot teach more than 4 courses simultaneously
- Course prerequisites must be satisfied before enrollment
- GPA calculation should exclude withdrawn courses
- Students with GPA < 2.0 are on academic probation

### Data Integrity Checks:
- Email addresses must be unique across all entities
- Course codes must follow format: DEPT###-### (e.g., CS101-001)
- Enrollment dates cannot be in the future
- Professor hire dates must be reasonable (not before 1950, not in future)

## Response Examples:

### Successful enrollment (201 Created)
```json
{
    "message": "Student successfully enrolled",
    "enrollment_id": "ENR123456",
    "student": {...},
    "course": {...},
    "enrollment_date": "2024-01-15"
}
```

### Capacity exceeded (409 Conflict)
```json
{
    "detail": "Course has reached maximum capacity",
    "error_code": "ENROLLMENT_CAPACITY_EXCEEDED",
    "available_capacity": 0,
    "current_enrollment": 30,
    "max_capacity": 30
}
```

### Validation error (422 Unprocessable Entity)
```json
{
    "detail": "Validation failed",
    "field_errors": {
        "gpa": ["ensure this value is less than or equal to 4.0"],
        "year": ["ensure this value is greater than or equal to 1"]
    }
}
```

## Submission Guidelines

### For All Problems:
- Follow REST API conventions and naming standards
- Implement comprehensive error handling
- Include proper docstrings and comments
- Use type hints throughout the code
- Ensure all test cases pass

### Problem 1 Specific:
- Demonstrate clear understanding of abstraction vs concrete implementation
- Show polymorphic behavior in action
- Implement proper inheritance hierarchies

### Problems 2 & 3 Specific:
- Use FastAPI best practices
- Implement proper request/response models
- Follow HTTP status code conventions
- Include API documentation via FastAPI's automatic docs

## Evaluation Criteria:
- **Code functionality and correctness (40%)**
- **Proper use of OOP principles (25%)**
- **API design and RESTful practices (20%)**
- **Error handling and validation (15%)**