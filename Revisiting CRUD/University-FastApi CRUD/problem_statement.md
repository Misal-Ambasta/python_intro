# Q: 2 - University Course Management System - FastAPI CRUD

## Problem Statement
Develop a RESTful API for a university course management system using FastAPI with a dictionary-based database. The system should manage students, courses, enrollments, and professors with full CRUD operations.

## Core Requirements

### Entities to Manage:
- **Students**: ID, name, email, major, year, GPA
- **Courses**: ID, name, code, credits, professor_id, max_capacity
- **Professors**: ID, name, email, department, hire_date
- **Enrollments**: student_id, course_id, enrollment_date, grade

### API Endpoints Structure:
- `/students`
- `/courses`
- `/professors`
- `/enrollments`

### CRUD Operations for Each Entity:
- **CREATE**: Add new records
- **READ**: Get all records and individual records
- **UPDATE**: Modify existing records
- **DELETE**: Remove records

## Functional Requirements

### Student Management:
- Register new students
- Update student information
- Calculate and update GPA based on course grades
- Get student's enrolled courses

### Course Management:
- Create courses with capacity limits
- Assign professors to courses
- Track enrollment count vs capacity
- Get course roster (enrolled students)

### Professor Management:
- Add professor profiles
- Assign courses to professors
- Get professor's teaching schedule

### Enrollment System:
- Enroll students in courses (with capacity checking)
- Record grades for completed courses
- Calculate semester/cumulative GPA
- Handle course withdrawals

## Expected API Endpoints

```http
GET /students                           # Get all students
POST /students                          # Create new student
GET /students/{id}                      # Get specific student
PUT /students/{id}                      # Update student
DELETE /students/{id}                   # Delete student
GET /students/{id}/courses              # Get student's courses

GET /courses                            # Get all courses
POST /courses                           # Create new course
GET /courses/{id}                       # Get specific course
PUT /courses/{id}                       # Update course
DELETE /courses/{id}                    # Delete course
GET /courses/{id}/students              # Get course roster

GET /professors                         # Get all professors
POST /professors                        # Create new professor
GET /professors/{id}                    # Get specific professor
PUT /professors/{id}                    # Update professor
DELETE /professors/{id}                 # Delete professor

POST /enrollments                       # Enroll student in course
GET /enrollments                        # Get all enrollments
PUT /enrollments/{student_id}/{course_id}    # Update grade
DELETE /enrollments/{student_id}/{course_id} # Drop course
```

## Business Logic to Implement
- Prevent enrollment if course is at capacity
- Validate professor exists when creating courses
- Calculate GPA automatically when grades are updated
- Ensure students can't enroll in same course twice
- Handle cascading deletes (if professor deleted, what happens to their courses?)