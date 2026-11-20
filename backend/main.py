
from fastapi import FastAPI, status
from pydantic import BaseModel

# Create the NECHO API application
app = FastAPI(
    title="NECHO API",
    description="AI-powered technology career guidance platform",
    version="0.1.0"
)


# ==============================
# PYDANTIC MODELS
# ==============================

class ChatRequest(BaseModel):
    message: str


class CareerGoalRequest(BaseModel):
    career_goal: str
    current_year: int


class CareerGoalResponse(BaseModel):
    student_id: int
    career_goal: str
    current_year: int
    message: str


class StudentCreate(BaseModel):
    name: str
    department: str
    current_year: int
class StudentUpdate(BaseModel):
    name: str
    department: str
    current_year: int
class StudentPartialUpdate(BaseModel):
    name: str | None = None
    department: str | None = None
    current_year: int | None = None

# ==============================
# ROOT AND HEALTH ENDPOINTS
# ==============================

@app.get("/")
async def root():
    return {
        "message": "Welcome to NECHO API!",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }


# ==============================
# CHAT ENDPOINT
# ==============================

@app.post("/api/chat")
async def chat(request: ChatRequest):
    return {
        "message_received": request.message,
        "reply": "NECHO received your message successfully!"
    }


# ==============================
# STUDENT ENDPOINTS
# ==============================

# Retrieve students using query parameters
@app.get("/students")
async def get_students(
    department: str = "all",
    year: int = 1
):
    return {
        "message": "Student information retrieved successfully",
        "department": department,
        "year": year
    }


# Receive new student information
@app.post("/students")
async def create_student(student: StudentCreate):
    return {
        "message": "Student information received successfully",
        "student": student
    }
@app.put("/students/{student_id}")
async def update_student(
    student_id: int,
    student: StudentUpdate
):
    return {
        "message": "Student replacement information received successfully",
        "student_id": student_id,
        "updated_student": student
    }
@app.patch("/students/{student_id}")
async def partial_update_student(
    student_id: int,
    student: StudentPartialUpdate
):
    return {
        "message": "Student partial update information received successfully",
        "student_id": student_id,
        "updated_fields": student.model_dump(exclude_unset=True)
    }
@app.delete("/students/{student_id}")
async def delete_student(student_id: int):
    return {
        "message": "Student deletion request received successfully",
        "student_id": student_id
    }
# Retrieve an individual student
@app.get("/students/{student_id}")
async def get_student(student_id: int):
    return {
        "student_id": student_id,
        "message": "Student information retrieved successfully"
    }


# Submit a student's career goal
@app.post(
    "/students/{student_id}/career-goal",
    response_model=CareerGoalResponse,
    status_code=status.HTTP_201_CREATED
)
async def save_career_goal(
    student_id: int,
    request: CareerGoalRequest
):
    return {
        "student_id": student_id,
        "career_goal": request.career_goal,
        "current_year": request.current_year,
        "message": "Career goal received successfully"
    }


# Retrieve a student's course
@app.get("/students/{student_id}/courses/{course_id}")
async def get_student_course(
    student_id: int,
    course_id: int
):
    return {
        "student_id": student_id,
        "course_id": course_id,
        "message": "Student course information retrieved successfully"
    }


# Retrieve course progress
@app.get("/students/{student_id}/courses/{course_id}/progress")
async def get_course_progress(
    student_id: int,
    course_id: int,
    include_progress: bool = True
):
    return {
        "student_id": student_id,
        "course_id": course_id,
        "include_progress": include_progress,
        "message": "Course progress retrieved successfully"
    }
