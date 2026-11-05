"""
Service xử lý nghiệp vụ khóa học.
"""
from sqlalchemy.orm import Session, joinedload

from models.course import Course
from models.course_category import CourseCategory
from schemas.course_schema import CourseCreate
from utils.exceptions import AppException


def get_all_courses(db: Session):
    """Lấy toàn bộ khóa học kèm thông tin danh mục khóa học."""
    return (
        db.query(Course)
        .options(joinedload(Course.course_category))
        .order_by(Course.id)
        .all()
    )


def create_course(db: Session, payload: CourseCreate) -> Course:
    """Thêm mới khóa học: kiểm tra danh mục khóa học tồn tại và mã khóa học không bị trùng."""
    type_obj = db.get(CourseCategory, payload.course_category_id)
    if type_obj is None:
        raise AppException(
            404, "Not Found",
            f"Không tìm thấy danh mục khóa học có id = {payload.course_category_id}",
        )

    duplicated = db.query(Course).filter(Course.course_code == payload.course_code).first()
    if duplicated is not None:
        raise AppException(
            409, "Conflict",
            f"Mã khóa học {payload.course_code} đã tồn tại",
        )

    new_course = Course(**payload.model_dump())
    db.add(new_course)
    db.commit()
    db.refresh(new_course)
    return new_course
