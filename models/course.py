"""
Model bảng courses (khóa học) - phía "N" của quan hệ 1-N.
"""
from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_code = Column(String(10), unique=True, nullable=False)
    tuition_fee = Column(Float, nullable=False)
    course_category_id = Column(Integer, ForeignKey("course_categories.id"), nullable=False)

    # Mỗi khóa học thuộc về một danh mục khóa học
    course_category = relationship("CourseCategory", back_populates="courses")
