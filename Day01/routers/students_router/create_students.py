from fastapi import APIRouter
from typing import Optional, List
from pydantic import BaseModel
from .db import user_list


router = APIRouter()


class Student(BaseModel):
    age: int  # Mandatory
    major: Optional[str] = None  # Optional
    gpa: Optional[float] = None  # Optional
    hobbies: Optional[List[str]] = None  # Optional


@router.post("/create/student/{student_name}")
async def create_single_student(student_name: str, student: Student):
    if student_name in user_list:
        return {"error": "Student already exists"}

    user_list[student_name] = student.model_dump()
    return {"message": f"Student '{student_name}' created successfully"}

