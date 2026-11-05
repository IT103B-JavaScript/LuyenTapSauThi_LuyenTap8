"""
Schemas Pydantic: validate dữ liệu đầu vào và định nghĩa cấu trúc dữ liệu đầu ra.
"""
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CourseCategoryResponse(BaseModel):
    """Thông tin danh mục khóa học trả về kèm trong khóa học."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class CourseCreate(BaseModel):
    """Dữ liệu đầu vào khi thêm mới khóa học."""
    course_code: str = Field(..., min_length=4, max_length=10, examples=["K301"])
    tuition_fee: float = Field(..., gt=0, examples=[3500000])
    course_category_id: int = Field(..., examples=[1])

    @field_validator("course_code")
    @classmethod
    def normalize_code(cls, value: str) -> str:
        """Bỏ khoảng trắng hai đầu, chuyển in hoa và kiểm tra lại độ dài."""
        value = value.strip().upper()
        if len(value) < 4:
            raise ValueError("Mã khóa học phải có ít nhất 4 ký tự")
        return value


class CourseResponse(BaseModel):
    """Thông tin khóa học trả về (dùng làm response_model)."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_code: str
    tuition_fee: float
    course_category: CourseCategoryResponse


class CourseListResponse(BaseModel):
    """Response chuẩn cho API lấy danh sách khóa học."""
    statusCode: int
    error: Optional[str] = None
    message: str
    data: List[CourseResponse]


class CourseDetailResponse(BaseModel):
    """Response chuẩn cho API trả về một khóa học."""
    statusCode: int
    error: Optional[str] = None
    message: str
    data: CourseResponse


class CourseCategoryDeleteResponse(BaseModel):
    """Response chuẩn cho API xóa danh mục khóa học."""
    statusCode: int
    error: Optional[str] = None
    message: str
    data: Optional[CourseCategoryResponse] = None
