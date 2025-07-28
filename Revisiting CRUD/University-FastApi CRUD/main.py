from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict, Optional
from datetime import date

app = FastAPI()


students_db: Dict[int, dict] = {}
courses_db: Dict[int, dict] = {}
professors_db: Dict[int, dict] = {}
enrollments_db: Dict[str, dict] = {}

class Student(BaseModel):
    id:int
    name:str
    email: EmailStr
    major: str
    year: int
    gpa: float = 0.0

class Course(BaseModel):
    id: int
    name: str
    code: str
    credits: int
    professor_id: int
    max_capacity: int

class Professor(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    hire_date: date

class Enrollment(BaseModel):
    student_id: int
    course_id: int
    enrollment_date: date
    grade: Optional[float] = None

@app.post("/students")
def create_student(student: Student):
    if student.id in students_db:
        raise HTTPException(status_code=400, detail="Student already exists")
    students_db[student.id] = student.dict()
    return student

@app.get("/students")
def get_all_students():
    return list(students_db.values())


@app.get("/students/{id}")
def get_students(id: int):
    if id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found.")
    return students_db[id]


@app.put("/students/{id}")
def update_student(id: int, updated_student: Student):
    if id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found")
    students_db[id] = update_student.dict()
    return update_student

@app.delete("students/{id}")
def delete_student(id: int):
    if id not in students_db:
        raise HTTPException(status_code=404, detail="Student not found.")
    del students_db[id]
    #remove enrollments
    global enrollments_db
    enrollments_db = {k: v for k, v in enrollments_db.items() if v['student_id'] != id}
    return {"detail": "Student deleted"}


@app.get("/students/{id}/course")
def get_student_courses(id: int):
    enrolled_courses = [e['course_id'] for e in enrollments_db.values() if e['student_id'] == id]
    return [courses_db[cid] for cid in enrolled_courses if cid in courses_db]

# ---------------- COURSES ------------------

@app.post("/courses")
def create_course(course: Course):
    if course.id in courses_db:
        raise HTTPException(status_code=400, detail="Course already exists.")
    if course.professor_id not in professors_db:
        raise HTTPException(status_code=404, detail="Professor not found.")
    courses_db[course.id] = course.dict()
    return course

@app.get("/courses")
def get_all_courses():
    return list(courses_db.values())

@app.get("/courses/{id}")
def get_course(id: int):
    if id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found.")
    return courses_db[id]

@app.put("/courses/{id}")
def update_course(id: int, updated_course: Course):
    if id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found.")
    if updated_course.professor_id not in professors_db:
        raise HTTPException(status_code=404, detail="Professor not found.")
    courses_db[id] = updated_course.dict()
    return updated_course

@app.delete("/courses/{id}")
def delete_course(id: int):
    if id not in courses_db:
        raise HTTPException(status_code=404, detail="Course not found.")
    del courses_db[id]
    global enrollments_db
    enrollments_db = {k: v for k, v in enrollments_db.items() if v['course_id'] != id}
    return {"detail": "Course deleted"}

@app.get("/courses/{id}/students")
def get_course_roster(id: int):
    students = [e['student_id'] for e in enrollments_db.values() if e['course_id'] == id]
    return [students_db[sid] for sid in students if sid in students_db]

# ---------------- PROFESSORS ------------------


@app.post("/professors")
def create_professor(professor: Professor):
    if professor.id in professors_db:
        raise HTTPException(status_code=400, detail="Professor already exists.")
    professors_db[professor.id] = professor.dict()
    return professor

@app.get("/professors")
def get_all_professors():
    return list(professors_db.values())

@app.get("/professors/{id}")
def get_professor(id: int):
    if id not in professors_db:
        raise HTTPException(status_code=404, detail="Professor not found.")
    return professors_db[id]

@app.put("/professors/{id}")
def update_professor(id: int, updated_prof: Professor):
    if id not in professors_db:
        raise HTTPException(status_code=404, detail="Professor not found.")
    professors_db[id] = updated_prof.dict()
    return updated_prof

@app.delete("/professors/{id}")
def delete_professor(id: int):
    if id not in professors_db:
        raise HTTPException(status_code=404, detail="Professor not found.")
    del professors_db[id]
    # Remove courses taught by this professor
    global courses_db, enrollments_db
    course_ids = [cid for cid, c in courses_db.items() if c['professor_id'] == id]
    for cid in course_ids:
        del courses_db[cid]
    enrollments_db = {k: v for k, v in enrollments_db.items() if v['course_id'] not in course_ids}
    return {"detail": "Professor and their courses deleted"}

# ---------------- ENROLLMENTS ------------------

@app.post("/enrollments")
def enroll_student(enrollment: Enrollment):
    if enrollment.student_id not in students_db or enrollment.course_id not in courses_db:
        raise HTTPException(status_code=404, detail="Student or Course not found.")
    
    key = f"{enrollment.student_id}_{enrollment.course_id}"
    if key in enrollments_db:
        raise HTTPException(status_code=400, detail="Student already enrolled.")
    
    # Capacity check
    current_enrolled = sum(1 for key, value in enrollments_db.items() if value['course_id'] == enrollment.course_id)
    if current_enrolled >= courses_db[enrollment.course_id]['max_capacity']:
        raise HTTPException(status_code=400, detail="Course at capacity.")
    
    enrollments_db[key] = enrollment.dict()
    return {"detail": "Enrolled successfully."}


@app.get("/enrollments")
def get_all_enrollments():
    return enrollments_db

@app.put("/enrollments/{student_id}/{course_id}")
def update_grade(student_id: int, course_id: int, grade: float):
    found = False
    for key, e in enrollments_db.items():
        if e['student_id'] == student_id and e['course_id'] == course_id:
            enrollments_db[key]['grade'] = grade
            found = True
            break
    if not found:
        raise HTTPException(status_code=404, detail="Enrollment not found.")
    update_student_gpa(student_id)
    return {"detail": "Grade updated and GPA recalculated."}

@app.delete("/enrollments/{student_id}/{course_id}")
def drop_course(student_id: int, course_id: int):
    global enrollments_db
    initial_len = len(enrollments_db)
    enrollments_db = {k: v for k, v in enrollments_db.items() if not (v['student_id'] == student_id and v['course_id'] == course_id)}
    if len(enrollments_db) == initial_len:
        raise HTTPException(status_code=404, detail="Enrollment not found.")
    update_student_gpa(student_id)
    return {"detail": "Course dropped."}

# ---------------- GPA CALCULATION ------------------

def update_student_gpa(student_id: int):
    grades = [e['grade'] for e in enrollments_db.values() if e['student_id'] == student_id and e.get('grade') is not None]
    gpa = round(sum(grades) / len(grades), 2) if grades else 0.0
    if student_id in students_db:
        students_db[student_id]['gpa'] = gpa

if __name__ == "__main__":
    uvicorn.run(app, port=8000)