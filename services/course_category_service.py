"""
Service xử lý nghiệp vụ danh mục khóa học.
"""
from sqlalchemy.orm import Session

from models.course import Course
from models.course_category import CourseCategory
from utils.exceptions import AppException

DEFAULT_COURSE_CATEGORIES = ["programming", "design", "marketing"]


def seed_default_course_categories(db: Session) -> None:
    """Tạo sẵn các danh mục khóa học mặc định nếu bảng đang trống (phục vụ test API)."""
    if db.query(CourseCategory).count() > 0:
        return
    for type_name in DEFAULT_COURSE_CATEGORIES:
        db.add(CourseCategory(name=type_name))
    db.commit()


def delete_course_category(db: Session, type_id: int) -> CourseCategory:
    """Xóa danh mục khóa học theo id, chỉ cho phép khi không còn khóa học nào thuộc loại này."""
    type_obj = db.get(CourseCategory, type_id)
    if type_obj is None:
        raise AppException(404, "Not Found", f"Không tìm thấy danh mục khóa học có id = {type_id}")

    total_courses = db.query(Course).filter(Course.course_category_id == type_id).count()
    if total_courses > 0:
        raise AppException(
            400, "Bad Request",
            f"Không thể xóa danh mục khóa học '{type_obj.name}' vì còn {total_courses} khóa học thuộc loại này",
        )

    db.delete(type_obj)
    db.commit()
    return type_obj
