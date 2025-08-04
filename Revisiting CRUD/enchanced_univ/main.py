from fastapi import FastAPI, HTTPException, Query, status, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime, date
from enum import Enum
import uuid
import re
from collections import defaultdict

app = FastAPI(
    title="Enhanced University Course Management System",
    description="A comprehensive system for managing students, courses, professors, and enrollments",
    version="0.1.0"
)

# ============= ENUMS =============

class GradeEnum(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    F = "F"

class MajorEnum(str, Enum):
    CS = "Computer Science"
    MATH = "Mathematics"
    PHYS = "Physics"
    CHEM = "Chemistry"
    ENG = "Engineering"
    BIO = "Biology"

class DepartmentEnum(str, Enum):
    CS = "Computer Science"
    MATH = "Mathematics"
    PHYS = "Physics"
    CHEM = "Chemistry"
    ENG = "Engineering"
    BIO = "Biology"

# ============= PYDANTIC MODELS =============

class StudentModel(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Student full name")
    email: EmailStr = Field(..., description="Student email address")
    major: MajorEnum = Field(..., description="Student major")
    year: int = Field(..., ge=1, le=4, description="Academic year (1-4)")
    gpa: float = Field(..., ge=0.0, le=4.0, description="Grade Point Average")
    
    @field_validator('name')
    def validate_name(cls, v):
        if not v.replace(' ', '').replace('-', '').replace("'", '').isalpha():
            raise ValueError('Name must contain only letters, spaces, hyphens, and apostrophes')
        return v.title()

class CourseModel(BaseModel):
    course_code: str = Field(..., description="Course code in format DEPT###-###")
    name: str = Field(..., min_length=5, max_length=200, description="Course name")
    department: DepartmentEnum = Field(..., description="Course department")
    credits: int = Field(..., ge=1, le=6, description="Credit hours (1-6)")
    capacity: int = Field(..., ge=1, le=500, description="Maximum enrollment capacity")
    prerequisites: List[str] = Field(default=[], description="List of prerequisite course codes")
    
    @field_validator('course_code')
    def validate_course_code(cls, v):
        pattern = r'^[A-Z]{2,4}\d{3}-\d{3}$'
        if not re.match(pattern, v):
            raise ValueError('Course code must follow format DEPT###-### (e.g., CS101-001)')
        return v.upper()

class ProfessorModel(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Professor full name")
    email: EmailStr = Field(..., description="Professor email address")
    department: DepartmentEnum = Field(..., description="Professor department")
    hire_date: date = Field(..., description="Date of hire")
    
    @field_validator('hire_date')
    def validate_hire_date(cls, v):
        if v > date.today():
            raise ValueError('Hire date cannot be in the future')
        if v.year < 1950:
            raise ValueError('Hire date must be after 1950')
        return v

class EnrollmentModel(BaseModel):
    student_id: str = Field(..., description="Student ID")
    course_id: str = Field(..., description="Course ID")
    grade: Optional[GradeEnum] = Field(None, description="Course grade")
    enrollment_date: date = Field(default_factory=date.today, description="Enrollment date")
    
    @field_validator('enrollment_date')
    def validate_enrollment_date(cls, v):
        if v > date.today():
            raise ValueError('Enrollment date cannot be in the future')
        return v

# ============= RESPONSE MODELS =============

class ErrorResponse(BaseModel):
    detail: str
    error_code: str
    field_errors: Optional[Dict[str, List[str]]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class PaginationResponse(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int
    has_next: bool
    has_prev: bool

class StudentResponse(StudentModel):
    id: str
    created_at: datetime
    is_on_probation: bool

class CourseResponse(CourseModel):
    id: str
    professor_id: Optional[str] = None
    current_enrollment: int
    created_at: datetime

class ProfessorResponse(ProfessorModel):
    id: str
    current_courses: List[str] = []
    created_at: datetime

class EnrollmentResponse(EnrollmentModel):
    id: str
    student_name: str
    course_name: str
    credits: int

# ============= IN-MEMORY STORAGE =============

students_db: Dict[str, Dict] = {}
courses_db: Dict[str, Dict] = {}
professors_db: Dict[str, Dict] = {}
enrollments_db: Dict[str, Dict] = {}
emails_registry: set = set()

# ============= UTILITY FUNCTIONS =============

def generate_id(prefix: str) -> str:
    """Generate unique ID with prefix"""
    return f"{prefix}{uuid.uuid4().hex[:8].upper()}"

def validate_unique_email(email: str, exclude_id: str = None) -> bool:
    """Check if email is unique across all entities"""
    for db in [students_db, professors_db]:
        for entity_id, entity in db.items():
            if entity_id != exclude_id and entity.get('email') == email:
                return False
    return True

def calculate_gpa(student_id: str) -> float:
    """Calculate student GPA based on completed courses"""
    grade_points = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
    total_points = 0
    total_credits = 0
    
    for enrollment in enrollments_db.values():
        if enrollment['student_id'] == student_id and enrollment.get('grade'):
            course = courses_db.get(enrollment['course_id'])
            if course:
                total_points += grade_points[enrollment['grade']] * course['credits']
                total_credits += course['credits']
    
    return total_points / total_credits if total_credits > 0 else 0.0

def get_student_credit_hours(student_id: str) -> int:
    """Get current semester credit hours for student"""
    total_credits = 0
    for enrollment in enrollments_db.values():
        if enrollment['student_id'] == student_id:
            course = courses_db.get(enrollment['course_id'])
            if course:
                total_credits += course['credits']
    return total_credits

def get_professor_teaching_load(professor_id: str) -> int:
    """Get current number of courses taught by professor"""
    return len([c for c in courses_db.values() if c.get('professor_id') == professor_id])

def check_prerequisites(student_id: str, course_id: str) -> bool:
    """Check if student has completed all prerequisites for a course"""
    course = courses_db.get(course_id)
    if not course or not course.get('prerequisites'):
        return True
    
    completed_courses = []
    for enrollment in enrollments_db.values():
        if (enrollment['student_id'] == student_id and 
            enrollment.get('grade') and enrollment['grade'] != 'F'):
            course_code = courses_db.get(enrollment['course_id'], {}).get('course_code')
            if course_code:
                completed_courses.append(course_code)
    
    return all(prereq in completed_courses for prereq in course['prerequisites'])

# ============= EXCEPTION HANDLERS =============

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            detail=exc.detail,
            error_code="HTTP_ERROR"
        ).dict()
    )

# ============= STUDENT ENDPOINTS =============

@app.post("/students", status_code=status.HTTP_201_CREATED, response_model=StudentResponse)
async def create_student(student: StudentModel):
    """Create a new student"""
    if not validate_unique_email(student.email):
        raise HTTPException(
            status_code=409,
            detail="Email address already exists in the system"
        )
    
    student_id = generate_id("STU")
    student_data = student.dict()
    student_data.update({
        'id': student_id,
        'created_at': datetime.utcnow(),
        'is_on_probation': student.gpa < 2.0
    })
    
    students_db[student_id] = student_data
    emails_registry.add(student.email)
    
    return StudentResponse(**student_data)

@app.get("/students", response_model=Dict[str, Any])
async def get_students(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    major: Optional[MajorEnum] = Query(None, description="Filter by major"),
    year: Optional[int] = Query(None, ge=1, le=4, description="Filter by year"),
    on_probation: Optional[bool] = Query(None, description="Filter by probation status")
):
    """Get students with pagination and filtering"""
    filtered_students = []
    
    for student in students_db.values():
        if major and student['major'] != major:
            continue
        if year and student['year'] != year:
            continue
        if on_probation is not None and student['is_on_probation'] != on_probation:
            continue
        filtered_students.append(StudentResponse(**student))
    
    total = len(filtered_students)
    start = (page - 1) * limit
    end = start + limit
    students_page = filtered_students[start:end]
    
    return {
        "students": students_page,
        "pagination": PaginationResponse(
            page=page,
            limit=limit,
            total=total,
            total_pages=(total + limit - 1) // limit,
            has_next=end < total,
            has_prev=page > 1
        )
    }

@app.get("/students/{student_id}", response_model=StudentResponse)
async def get_student(student_id: str):
    """Get a specific student"""
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return StudentResponse(**students_db[student_id])

@app.put("/students/{student_id}", response_model=StudentResponse)
async def update_student(student_id: str, student: StudentModel):
    """Update a student"""
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    
    if not validate_unique_email(student.email, student_id):
        raise HTTPException(
            status_code=409,
            detail="Email address already exists in the system"
        )
    
    # Remove old email and add new one
    old_email = students_db[student_id]['email']
    emails_registry.discard(old_email)
    emails_registry.add(student.email)
    
    student_data = student.dict()
    student_data.update({
        'id': student_id,
        'created_at': students_db[student_id]['created_at'],
        'is_on_probation': student.gpa < 2.0
    })
    
    students_db[student_id] = student_data
    return StudentResponse(**student_data)

@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(student_id: str):
    """Delete a student"""
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Remove all enrollments for this student
    enrollments_to_remove = [
        eid for eid, enrollment in enrollments_db.items() 
        if enrollment['student_id'] == student_id
    ]
    for eid in enrollments_to_remove:
        del enrollments_db[eid]
    
    # Remove email from registry
    emails_registry.discard(students_db[student_id]['email'])
    del students_db[student_id]

# ============= COURSE ENDPOINTS =============

@app.post("/courses", status_code=status.HTTP_201_CREATED, response_model=CourseResponse)
async def create_course(course: CourseModel):
    """Create a new course"""
    # Check for duplicate course code
    for existing_course in courses_db.values():
        if existing_course['course_code'] == course.course_code:
            raise HTTPException(
                status_code=409,
                detail="Course code already exists"
            )
    
    course_id = generate_id("CRS")
    course_data = course.dict()
    course_data.update({
        'id': course_id,
        'current_enrollment': 0,
        'created_at': datetime.utcnow()
    })
    
    courses_db[course_id] = course_data
    return CourseResponse(**course_data)

@app.get("/courses", response_model=Dict[str, Any])
async def get_courses(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    department: Optional[DepartmentEnum] = Query(None),
    credits: Optional[int] = Query(None, ge=1, le=6)
):
    """Get courses with pagination and filtering"""
    filtered_courses = []
    
    for course in courses_db.values():
        if department and course['department'] != department:
            continue
        if credits and course['credits'] != credits:
            continue
        filtered_courses.append(CourseResponse(**course))
    
    total = len(filtered_courses)
    start = (page - 1) * limit
    end = start + limit
    courses_page = filtered_courses[start:end]
    
    return {
        "courses": courses_page,
        "pagination": PaginationResponse(
            page=page,
            limit=limit,
            total=total,
            total_pages=(total + limit - 1) // limit,
            has_next=end < total,
            has_prev=page > 1
        )
    }

@app.get("/courses/{course_id}", response_model=CourseResponse)
async def get_course(course_id: str):
    """Get a specific course"""
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    
    return CourseResponse(**courses_db[course_id])

@app.put("/courses/{course_id}", response_model=CourseResponse)
async def update_course(course_id: str, course: CourseModel):
    """Update a course"""
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check for duplicate course code (excluding current course)
    for existing_id, existing_course in courses_db.items():
        if existing_id != course_id and existing_course['course_code'] == course.course_code:
            raise HTTPException(
                status_code=409,
                detail="Course code already exists"
            )
    
    course_data = course.dict()
    course_data.update({
        'id': course_id,
        'current_enrollment': courses_db[course_id]['current_enrollment'],
        'created_at': courses_db[course_id]['created_at'],
        'professor_id': courses_db[course_id].get('professor_id')
    })
    
    courses_db[course_id] = course_data
    return CourseResponse(**course_data)

@app.delete("/courses/{course_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_course(course_id: str):
    """Delete a course"""
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Remove all enrollments for this course
    enrollments_to_remove = [
        eid for eid, enrollment in enrollments_db.items() 
        if enrollment['course_id'] == course_id
    ]
    for eid in enrollments_to_remove:
        del enrollments_db[eid]
    
    del courses_db[course_id]

# ============= PROFESSOR ENDPOINTS =============

@app.post("/professors", status_code=status.HTTP_201_CREATED, response_model=ProfessorResponse)
async def create_professor(professor: ProfessorModel):
    """Create a new professor"""
    if not validate_unique_email(professor.email):
        raise HTTPException(
            status_code=409,
            detail="Email address already exists in the system"
        )
    
    professor_id = generate_id("PRF")
    professor_data = professor.dict()
    professor_data.update({
        'id': professor_id,
        'current_courses': [],
        'created_at': datetime.utcnow()
    })
    
    professors_db[professor_id] = professor_data
    emails_registry.add(professor.email)
    
    return ProfessorResponse(**professor_data)

@app.get("/professors", response_model=Dict[str, Any])
async def get_professors(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    department: Optional[DepartmentEnum] = Query(None),
    hire_year: Optional[int] = Query(None, ge=1950)
):
    """Get professors with pagination and filtering"""
    filtered_professors = []
    
    for professor in professors_db.values():
        if department and professor['department'] != department:
            continue
        if hire_year and professor['hire_date'].year != hire_year:
            continue
        
        # Update current courses
        current_courses = [
            c['id'] for c in courses_db.values() 
            if c.get('professor_id') == professor['id']
        ]
        professor['current_courses'] = current_courses
        
        filtered_professors.append(ProfessorResponse(**professor))
    
    total = len(filtered_professors)
    start = (page - 1) * limit
    end = start + limit
    professors_page = filtered_professors[start:end]
    
    return {
        "professors": professors_page,
        "pagination": PaginationResponse(
            page=page,
            limit=limit,
            total=total,
            total_pages=(total + limit - 1) // limit,
            has_next=end < total,
            has_prev=page > 1
        )
    }

@app.get("/professors/{professor_id}", response_model=ProfessorResponse)
async def get_professor(professor_id: str):
    """Get a specific professor"""
    if professor_id not in professors_db:
        raise HTTPException(status_code=404, detail="Professor not found")
    
    professor_data = professors_db[professor_id].copy()
    current_courses = [
        c['id'] for c in courses_db.values() 
        if c.get('professor_id') == professor_id
    ]
    professor_data['current_courses'] = current_courses
    
    return ProfessorResponse(**professor_data)

# ============= ENROLLMENT ENDPOINTS =============

@app.post("/enrollments", status_code=status.HTTP_201_CREATED)
async def create_enrollment(enrollment: EnrollmentModel):
    """Enroll a student in a course"""
    # Validate student exists
    if enrollment.student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    
    # Validate course exists
    if enrollment.course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    
    # Check for duplicate enrollment
    for existing_enrollment in enrollments_db.values():
        if (existing_enrollment['student_id'] == enrollment.student_id and
            existing_enrollment['course_id'] == enrollment.course_id):
            raise HTTPException(
                status_code=409,
                detail="Student is already enrolled in this course"
            )
    
    course = courses_db[enrollment.course_id]
    student = students_db[enrollment.student_id]
    
    # Check course capacity
    if course['current_enrollment'] >= course['capacity']:
        raise HTTPException(
            status_code=409,
            detail="Course has reached maximum capacity",
            headers={
                "X-Error-Code": "ENROLLMENT_CAPACITY_EXCEEDED",
                "X-Available-Capacity": "0",
                "X-Current-Enrollment": str(course['current_enrollment']),
                "X-Max-Capacity": str(course['capacity'])
            }
        )
    
    # Check student credit limit (18 hours max)
    current_credits = get_student_credit_hours(enrollment.student_id)
    if current_credits + course['credits'] > 18:
        raise HTTPException(
            status_code=409,
            detail=f"Enrollment would exceed 18 credit hour limit. Current: {current_credits}, Course: {course['credits']}"
        )
    
    # Check prerequisites
    if not check_prerequisites(enrollment.student_id, enrollment.course_id):
        raise HTTPException(
            status_code=409,
            detail="Student has not completed required prerequisites"
        )
    
    # Create enrollment
    enrollment_id = generate_id("ENR")
    enrollment_data = enrollment.dict()
    enrollment_data.update({
        'id': enrollment_id,
        'student_name': student['name'],
        'course_name': course['name'],
        'credits': course['credits']
    })
    
    enrollments_db[enrollment_id] = enrollment_data
    courses_db[enrollment.course_id]['current_enrollment'] += 1
    
    return {
        "message": "Student successfully enrolled",
        "enrollment_id": enrollment_id,
        "student": student,
        "course": course,
        "enrollment_date": enrollment.enrollment_date.isoformat()
    }

@app.get("/enrollments", response_model=List[EnrollmentResponse])
async def get_enrollments(
    student_id: Optional[str] = Query(None),
    course_id: Optional[str] = Query(None)
):
    """Get enrollments with optional filtering"""
    filtered_enrollments = []
    
    for enrollment in enrollments_db.values():
        if student_id and enrollment['student_id'] != student_id:
            continue
        if course_id and enrollment['course_id'] != course_id:
            continue
        filtered_enrollments.append(EnrollmentResponse(**enrollment))
    
    return filtered_enrollments

@app.put("/enrollments/grades/{enrollment_id}")
async def update_grade(enrollment_id: str, grade: GradeEnum):
    """Update student grade for an enrollment"""
    if enrollment_id not in enrollments_db:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    
    enrollments_db[enrollment_id]['grade'] = grade
    
    # Update student probation status based on new GPA
    student_id = enrollments_db[enrollment_id]['student_id']
    new_gpa = calculate_gpa(student_id)
    students_db[student_id]['gpa'] = new_gpa
    students_db[student_id]['is_on_probation'] = new_gpa < 2.0
    
    return {"message": "Grade updated successfully", "grade": grade}

# ============= ANALYTICS ENDPOINTS =============

@app.get("/analytics/students/gpa-distribution")
async def get_gpa_distribution():
    """Get GPA distribution analytics"""
    gpa_ranges = {
        "4.0": 0, "3.5-3.99": 0, "3.0-3.49": 0, 
        "2.5-2.99": 0, "2.0-2.49": 0, "Below 2.0": 0
    }
    
    for student in students_db.values():
        gpa = student['gpa']
        if gpa == 4.0:
            gpa_ranges["4.0"] += 1
        elif gpa >= 3.5:
            gpa_ranges["3.5-3.99"] += 1
        elif gpa >= 3.0:
            gpa_ranges["3.0-3.49"] += 1
        elif gpa >= 2.5:
            gpa_ranges["2.5-2.99"] += 1
        elif gpa >= 2.0:
            gpa_ranges["2.0-2.49"] += 1
        else:
            gpa_ranges["Below 2.0"] += 1
    
    return {
        "total_students": len(students_db),
        "gpa_distribution": gpa_ranges,
        "average_gpa": sum(s['gpa'] for s in students_db.values()) / len(students_db) if students_db else 0,
        "students_on_probation": sum(1 for s in students_db.values() if s['is_on_probation'])
    }

@app.get("/analytics/courses/enrollment-stats")
async def get_enrollment_stats():
    """Get course enrollment statistics"""
    stats = []
    
    for course in courses_db.values():
        enrollment_rate = (course['current_enrollment'] / course['capacity']) * 100
        stats.append({
            "course_id": course['id'],
            "course_code": course['course_code'],
            "course_name": course['name'],
            "department": course['department'],
            "capacity": course['capacity'],
            "current_enrollment": course['current_enrollment'],
            "enrollment_rate": round(enrollment_rate, 2),
            "available_spots": course['capacity'] - course['current_enrollment']
        })
    
    # Sort by enrollment rate descending
    stats.sort(key=lambda x: x['enrollment_rate'], reverse=True)
    
    return {
        "total_courses": len(courses_db),
        "course_stats": stats,
        "overall_enrollment_rate": round(
            sum(c['current_enrollment'] for c in courses_db.values()) / 
            sum(c['capacity'] for c in courses_db.values()) * 100, 2
        ) if courses_db else 0
    }

@app.get("/analytics/professors/teaching-load")
async def get_teaching_load():
    """Get professor teaching load analytics"""
    load_stats = []
    
    for professor in professors_db.values():
        teaching_load = get_professor_teaching_load(professor['id'])
        total_students = sum(
            c['current_enrollment'] for c in courses_db.values() 
            if c.get('professor_id') == professor['id']
        )
        
        load_stats.append({
            "professor_id": professor['id'],
            "professor_name": professor['name'],
            "department": professor['department'],
            "courses_taught": teaching_load,
            "total_students": total_students,
            "load_status": "Overloaded" if teaching_load > 4 else "Normal"
        })
    
    return {
        "total_professors": len(professors_db),
        "teaching_loads": load_stats,
        "overloaded_professors": len([p for p in load_stats if p['load_status'] == 'Overloaded'])
    }

@app.get("/analytics/departments/performance")
async def get_department_performance():
    """Get department performance analytics"""
    dept_stats = defaultdict(lambda: {
        'students': 0, 'courses': 0, 'professors': 0, 
        'total_gpa': 0, 'total_enrollment': 0
    })
    
    # Count students by major
    for student in students_db.values():
        dept = student['major']
        dept_stats[dept]['students'] += 1
        dept_stats[dept]['total_gpa'] += student['gpa']
    
    # Count courses and enrollment by department
    for course in courses_db.values():
        dept = course['department']
        dept_stats[dept]['courses'] += 1
        dept_stats[dept]['total_enrollment'] += course['current_enrollment']
    
    # Count professors by department
    for professor in professors_db.values():
        dept = professor['department']
        dept_stats[dept]['professors'] += 1
    
    # Calculate averages
    performance_data = []
    for dept, stats in dept_stats.items():
        avg_gpa = stats['total_gpa'] / stats['students'] if stats['students'] > 0 else 0
        avg_enrollment = stats['total_enrollment'] / stats['courses'] if stats['courses'] > 0 else 0
        
        performance_data.append({
            "department": dept,
            "total_students": stats['students'],
            "total_courses": stats['courses'],
            "total_professors": stats['professors'],
            "average_gpa": round(avg_gpa, 2),
            "average_course_enrollment": round(avg_enrollment, 2)
        })
    
    return {"department_performance": performance_data}

# ============= BULK OPERATIONS =============
@app.post("/students/bulk", status_code=status.HTTP_201_CREATED)
async def bulk_create_students(students: List[StudentModel]):
    """Bulk create students"""
    created_students = []
    errors = []
    
    for i, student in enumerate(students):
        try:
            if not validate_unique_email(student.email):
                errors.append({
                    "index": i,
                    "email": student.email,
                    "error": "Email already exists"
                })
                continue
            
            student_id = generate_id("STU")
            student_data = student.dict()
            student_data.update({
                'id': student_id,
                'created_at': datetime.utcnow(),
                'is_on_probation': student.gpa < 2.0
            })
            
            students_db[student_id] = student_data
            emails_registry.add(student.email)
            created_students.append(StudentResponse(**student_data))
            
        except Exception as e:
            errors.append({
                "index": i,
                "email": student.email,
                "error": str(e)
            })
    
    return {
        "created_count": len(created_students),
        "error_count": len(errors),
        "created_students": created_students,
        "errors": errors
    }

@app.post("/enrollments/bulk", status_code=status.HTTP_201_CREATED)
async def bulk_create_enrollments(enrollments: List[EnrollmentModel]):
    """Bulk create enrollments"""
    created_enrollments = []
    errors = []
    
    for i, enrollment in enumerate(enrollments):
        try:
            # Validate student exists
            if enrollment.student_id not in students_db:
                errors.append({
                    "index": i,
                    "student_id": enrollment.student_id,
                    "course_id": enrollment.course_id,
                    "error": "Student not found"
                })
                continue
            
            # Validate course exists
            if enrollment.course_id not in courses_db:
                errors.append({
                    "index": i,
                    "student_id": enrollment.student_id,
                    "course_id": enrollment.course_id,
                    "error": "Course not found"
                })
                continue
            
            # Check for duplicate enrollment
            duplicate_found = False
            for existing_enrollment in enrollments_db.values():
                if (existing_enrollment['student_id'] == enrollment.student_id and
                    existing_enrollment['course_id'] == enrollment.course_id):
                    errors.append({
                        "index": i,
                        "student_id": enrollment.student_id,
                        "course_id": enrollment.course_id,
                        "error": "Student already enrolled in course"
                    })
                    duplicate_found = True
                    break
            
            if duplicate_found:
                continue
            
            course = courses_db[enrollment.course_id]
            student = students_db[enrollment.student_id]
            
            # Check course capacity
            if course['current_enrollment'] >= course['capacity']:
                errors.append({
                    "index": i,
                    "student_id": enrollment.student_id,
                    "course_id": enrollment.course_id,
                    "error": "Course at maximum capacity"
                })
                continue
            
            # Check student credit limit
            current_credits = get_student_credit_hours(enrollment.student_id)
            if current_credits + course['credits'] > 18:
                errors.append({
                    "index": i,
                    "student_id": enrollment.student_id,
                    "course_id": enrollment.course_id,
                    "error": f"Would exceed 18 credit limit (current: {current_credits})"
                })
                continue
            
            # Check prerequisites
            if not check_prerequisites(enrollment.student_id, enrollment.course_id):
                errors.append({
                    "index": i,
                    "student_id": enrollment.student_id,
                    "course_id": enrollment.course_id,
                    "error": "Prerequisites not met"
                })
                continue
            
            # Create enrollment
            enrollment_id = generate_id("ENR")
            enrollment_data = enrollment.dict()
            enrollment_data.update({
                'id': enrollment_id,
                'student_name': student['name'],
                'course_name': course['name'],
                'credits': course['credits']
            })
            
            enrollments_db[enrollment_id] = enrollment_data
            courses_db[enrollment.course_id]['current_enrollment'] += 1
            created_enrollments.append(EnrollmentResponse(**enrollment_data))
            
        except Exception as e:
            errors.append({
                "index": i,
                "student_id": enrollment.student_id,
                "course_id": enrollment.course_id,
                "error": str(e)
            })
    
    return {
        "created_count": len(created_enrollments),
        "error_count": len(errors),
        "created_enrollments": created_enrollments,
        "errors": errors
    }

@app.put("/enrollments/grades/bulk")
async def bulk_update_grades(grade_updates: List[Dict[str, Any]]):
    """Bulk update grades for enrollments"""
    updated_enrollments = []
    errors = []
    
    for i, update in enumerate(grade_updates):
        try:
            enrollment_id = update.get('enrollment_id')
            grade = update.get('grade')
            
            if not enrollment_id or not grade:
                errors.append({
                    "index": i,
                    "error": "Missing enrollment_id or grade"
                })
                continue
            
            if enrollment_id not in enrollments_db:
                errors.append({
                    "index": i,
                    "enrollment_id": enrollment_id,
                    "error": "Enrollment not found"
                })
                continue
            
            if grade not in ['A', 'B', 'C', 'D', 'F']:
                errors.append({
                    "index": i,
                    "enrollment_id": enrollment_id,
                    "error": "Invalid grade"
                })
                continue
            
            # Update grade
            enrollments_db[enrollment_id]['grade'] = grade
            
            # Update student GPA and probation status
            student_id = enrollments_db[enrollment_id]['student_id']
            new_gpa = calculate_gpa(student_id)
            students_db[student_id]['gpa'] = new_gpa
            students_db[student_id]['is_on_probation'] = new_gpa < 2.0
            
            updated_enrollments.append({
                "enrollment_id": enrollment_id,
                "student_id": student_id,
                "grade": grade,
                "new_gpa": round(new_gpa, 2)
            })
            
        except Exception as e:
            errors.append({
                "index": i,
                "error": str(e)
            })
    
    return {
        "updated_count": len(updated_enrollments),
        "error_count": len(errors),
        "updated_enrollments": updated_enrollments,
        "errors": errors
    }

# ============= COURSE ASSIGNMENT ENDPOINTS =============

@app.put("/courses/{course_id}/assign-professor/{professor_id}")
async def assign_professor_to_course(course_id: str, professor_id: str):
    """Assign a professor to a course"""
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if professor_id not in professors_db:
        raise HTTPException(status_code=404, detail="Professor not found")
    
    # Check if professor already has maximum teaching load
    current_load = get_professor_teaching_load(professor_id)
    if current_load >= 4:
        raise HTTPException(
            status_code=409,
            detail=f"Professor already teaching maximum of 4 courses (current: {current_load})"
        )
    
    # Check if course already has a professor
    if courses_db[course_id].get('professor_id'):
        old_professor_id = courses_db[course_id]['professor_id']
        old_professor_name = professors_db.get(old_professor_id, {}).get('name', 'Unknown')
        return {
            "message": f"Course reassigned from {old_professor_name} to {professors_db[professor_id]['name']}",
            "previous_professor": old_professor_name,
            "new_professor": professors_db[professor_id]['name']
        }
    
    courses_db[course_id]['professor_id'] = professor_id
    
    return {
        "message": "Professor successfully assigned to course",
        "course": courses_db[course_id]['name'],
        "professor": professors_db[professor_id]['name']
    }

@app.delete("/courses/{course_id}/unassign-professor", status_code=status.HTTP_204_NO_CONTENT)
async def unassign_professor_from_course(course_id: str):
    """Remove professor assignment from a course"""
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    
    if 'professor_id' in courses_db[course_id]:
        del courses_db[course_id]['professor_id']

# ============= UTILITY ENDPOINTS =============

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow(),
        "version": "2.0.0",
        "database_stats": {
            "students": len(students_db),
            "courses": len(courses_db),
            "professors": len(professors_db),
            "enrollments": len(enrollments_db)
        }
    }

@app.post("/admin/seed-data")
async def seed_sample_data():
    """Seed the database with sample data for testing"""
    # Clear existing data
    students_db.clear()
    courses_db.clear()
    professors_db.clear()
    enrollments_db.clear()
    emails_registry.clear()
    
    # Sample students
    sample_students = [
        {"name": "Alice Johnson", "email": "alice.johnson@university.edu", "major": "Computer Science", "year": 2, "gpa": 3.8},
        {"name": "Bob Smith", "email": "bob.smith@university.edu", "major": "Mathematics", "year": 3, "gpa": 3.2},
        {"name": "Carol Davis", "email": "carol.davis@university.edu", "major": "Physics", "year": 1, "gpa": 3.9},
        {"name": "David Wilson", "email": "david.wilson@university.edu", "major": "Computer Science", "year": 4, "gpa": 2.1},
        {"name": "Eva Brown", "email": "eva.brown@university.edu", "major": "Chemistry", "year": 2, "gpa": 3.5}
    ]
    
    for student_data in sample_students:
        student_id = generate_id("STU")
        student_data.update({
            'id': student_id,
            'created_at': datetime.utcnow(),
            'is_on_probation': student_data['gpa'] < 2.0
        })
        students_db[student_id] = student_data
        emails_registry.add(student_data['email'])
    
    # Sample professors
    sample_professors = [
        {"name": "Dr. Sarah Miller", "email": "s.miller@university.edu", "department": "Computer Science", "hire_date": date(2015, 8, 15)},
        {"name": "Prof. Michael Chen", "email": "m.chen@university.edu", "department": "Mathematics", "hire_date": date(2010, 1, 20)},
        {"name": "Dr. Lisa Anderson", "email": "l.anderson@university.edu", "department": "Physics", "hire_date": date(2018, 9, 1)}
    ]
    
    for prof_data in sample_professors:
        prof_id = generate_id("PRF")
        prof_data.update({
            'id': prof_id,
            'current_courses': [],
            'created_at': datetime.utcnow()
        })
        professors_db[prof_id] = prof_data
        emails_registry.add(prof_data['email'])
    
    # Sample courses
    sample_courses = [
        {"course_code": "CS101-001", "name": "Introduction to Programming", "department": "Computer Science", "credits": 3, "capacity": 30, "prerequisites": []},
        {"course_code": "CS201-001", "name": "Data Structures", "department": "Computer Science", "credits": 4, "capacity": 25, "prerequisites": ["CS101-001"]},
        {"course_code": "MATH101-001", "name": "Calculus I", "department": "Mathematics", "credits": 4, "capacity": 40, "prerequisites": []},
        {"course_code": "PHYS101-001", "name": "General Physics", "department": "Physics", "credits": 3, "capacity": 35, "prerequisites": []}
    ]
    
    course_ids = []
    for course_data in sample_courses:
        course_id = generate_id("CRS")
        course_data.update({
            'id': course_id,
            'current_enrollment': 0,
            'created_at': datetime.utcnow()
        })
        courses_db[course_id] = course_data
        course_ids.append(course_id)
    
    # Assign professors to courses
    prof_ids = list(professors_db.keys())
    for i, course_id in enumerate(course_ids):
        if i < len(prof_ids):
            courses_db[course_id]['professor_id'] = prof_ids[i]
    
    return {
        "message": "Sample data seeded successfully",
        "students_created": len(sample_students),
        "professors_created": len(sample_professors),
        "courses_created": len(sample_courses)
    }

@app.delete("/admin/clear-data", status_code=status.HTTP_204_NO_CONTENT)
async def clear_all_data():
    """Clear all data from the system (for testing purposes)"""
    students_db.clear()
    courses_db.clear()
    professors_db.clear()
    enrollments_db.clear()
    emails_registry.clear()

# ============= ADVANCED SEARCH ENDPOINTS =============

@app.get("/search/students")
async def search_students(
    q: str = Query(..., min_length=2, description="Search query"),
    field: str = Query("name", regex="^(name|email|major)$", description="Field to search in")
):
    """Advanced student search"""
    results = []
    query_lower = q.lower()
    
    for student in students_db.values():
        field_value = str(student.get(field, "")).lower()
        if query_lower in field_value:
            results.append(StudentResponse(**student))
    
    return {
        "query": q,
        "field": field,
        "total_results": len(results),
        "results": results
    }

@app.get("/search/courses")
async def search_courses(
    q: str = Query(..., min_length=2),
    field: str = Query("name", regex="^(name|course_code|department)$")
):
    """Advanced course search"""
    results = []
    query_lower = q.lower()
    
    for course in courses_db.values():
        field_value = str(course.get(field, "")).lower()
        if query_lower in field_value:
            results.append(CourseResponse(**course))
    
    return {
        "query": q,
        "field": field,
        "total_results": len(results),
        "results": results
    }

# ============= REPORTING ENDPOINTS =============

@app.get("/reports/transcript/{student_id}")
async def get_student_transcript(student_id: str):
    """Generate student transcript"""
    if student_id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student = students_db[student_id]
    student_enrollments = []
    total_credits = 0
    total_grade_points = 0
    
    grade_points = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0}
    
    for enrollment in enrollments_db.values():
        if enrollment['student_id'] == student_id:
            course = courses_db.get(enrollment['course_id'], {})
            enrollment_record = {
                "course_code": course.get('course_code', 'N/A'),
                "course_name": course.get('name', 'N/A'),
                "credits": course.get('credits', 0),
                "grade": enrollment.get('grade', 'In Progress'),
                "enrollment_date": enrollment.get('enrollment_date')
            }
            
            if enrollment.get('grade'):
                total_credits += course.get('credits', 0)
                total_grade_points += grade_points[enrollment['grade']] * course.get('credits', 0)
            
            student_enrollments.append(enrollment_record)
    
    cumulative_gpa = total_grade_points / total_credits if total_credits > 0 else 0.0
    
    return {
        "student_info": {
            "name": student['name'],
            "email": student['email'],
            "major": student['major'],
            "year": student['year'],
            "student_id": student_id
        },
        "academic_summary": {
            "total_credits_completed": total_credits,
            "cumulative_gpa": round(cumulative_gpa, 2),
            "academic_standing": "Good Standing" if cumulative_gpa >= 2.0 and not student['is_on_probation'] else "Academic Probation"
        },
        "course_history": student_enrollments,
        "generated_at": datetime.utcnow()
    }

@app.get("/reports/course-roster/{course_id}")
async def get_course_roster(course_id: str):
    """Generate course roster"""
    if course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found")
    
    course = courses_db[course_id]
    enrolled_students = []
    
    for enrollment in enrollments_db.values():
        if enrollment['course_id'] == course_id:
            student = students_db.get(enrollment['student_id'], {})
            enrolled_students.append({
                "student_id": enrollment['student_id'],
                "name": student.get('name', 'N/A'),
                "email": student.get('email', 'N/A'),
                "year": student.get('year', 'N/A'),
                "major": student.get('major', 'N/A'),
                "grade": enrollment.get('grade', 'In Progress'),
                "enrollment_date": enrollment.get('enrollment_date')
            })
    
    # Sort by student name
    enrolled_students.sort(key=lambda x: x['name'])
    
    professor_info = {}
    if course.get('professor_id'):
        professor = professors_db.get(course['professor_id'], {})
        professor_info = {
            "name": professor.get('name', 'N/A'),
            "email": professor.get('email', 'N/A')
        }
    
    return {
        "course_info": {
            "course_code": course['course_code'],
            "name": course['name'],
            "department": course['department'],
            "credits": course['credits'],
            "capacity": course['capacity'],
            "current_enrollment": course['current_enrollment']
        },
        "professor": professor_info,
        "enrolled_students": enrolled_students,
        "enrollment_summary": {
            "total_enrolled": len(enrolled_students),
            "available_spots": course['capacity'] - len(enrolled_students),
            "enrollment_rate": round((len(enrolled_students) / course['capacity']) * 100, 2)
        },
        "generated_at": datetime.utcnow()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)