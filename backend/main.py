
from fastapi import FastAPI
from pydantic import BaseModel

# Create the NECHO API application
app = FastAPI(
    title="NECHO API",
    description="AI-powered technology career guidance platform",
    version="0.1.0"
)


# Define the structure of a chat message
class ChatRequest(BaseModel):
    message: str


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to NECHO API!",
        "status": "running"
    }


# Health-check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy"
    }


# Chat endpoint
@app.post("/api/chat")
async def chat(request: ChatRequest):

    return {
        "message_received": request.message,
        "reply": "NECHO received your message successfully!"
    }

# Student endpoint using a path parameter
@app.get("/students/{student_id}")
async def get_student(student_id: int):

    return {
        "student_id": student_id,
        "message": "Student information retrieved successfully"
    }
# Students endpoint using a query parameter
@app.get("/students")
async def get_students(
    department: str = "all",
    year: int = 1
):
    return {
        "department": department,
        "year": year
    }
@app.get("/students/{student_id}/courses/{course_id}")
async def get_student_course(student_id: int, course_id: int):

    return {
        "student_id": student_id,
        "course_id": course_id,
        "message": "Student course information retrieved successfully"
    }