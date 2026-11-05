"""Gom các model để SQLAlchemy nhận diện đầy đủ quan hệ khi tạo bảng."""
from models.course_category import CourseCategory
from models.course import Course

__all__ = ["CourseCategory", "Course"]
