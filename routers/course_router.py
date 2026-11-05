"""
Router API khóa học: GET /courses, POST /courses
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database import get_db
from schemas.course_schema import CourseCreate, CourseDetailResponse, CourseListResponse
from services import course_service

router = APIRouter(prefix="/courses", tags=["Khóa học"])


@router.get("", response_model=CourseListResponse, status_code=status.HTTP_200_OK)
def get_courses(db: Session = Depends(get_db)):
    """API 2: Truy vấn danh sách khóa học kèm chi tiết danh mục khóa học."""
    items = course_service.get_all_courses(db)
    return {
        "statusCode": 200,
        "error": None,
        "message": "Lấy danh sách khóa học thành công",
        "data": items,
    }


@router.post("", response_model=CourseDetailResponse, status_code=status.HTTP_201_CREATED)
def create_course(payload: CourseCreate, db: Session = Depends(get_db)):
    """API 1: Thêm mới một khóa học."""
    new_item = course_service.create_course(db, payload)
    return {
        "statusCode": 201,
        "error": None,
        "message": "Thêm mới khóa học thành công",
        "data": new_item,
    }
