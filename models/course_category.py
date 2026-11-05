"""
Model bảng course_categories (danh mục khóa học) - phía "1" của quan hệ 1-N.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class CourseCategory(Base):
    __tablename__ = "course_categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)

    # Một danh mục khóa học có nhiều khóa học
    courses = relationship("Course", back_populates="course_category")
