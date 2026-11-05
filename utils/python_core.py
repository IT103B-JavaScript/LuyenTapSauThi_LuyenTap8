"""
Phần 1: Python Core & Tư duy thuật toán
- Yêu cầu 1.1: clean_and_validate_courses
- Yêu cầu 1.2: search_courses (Linear Search)
- Yêu cầu 1.3: sort_courses_by_tuition_fee_desc (Bubble Sort)
Chạy thử: python -m utils.python_core
"""

raw_courses = [
    {"course_code": "K101", "category": "programming",
     "tuition_fee": 3500000, "status": "open"},
    {"course_code": " k102 ", "category": "design",
     "tuition_fee": 2800000, "status": "open"},
    {"course_code": "K201", "category": "marketing",
     "tuition_fee": 2000000, "status": "closed"},
    {"course_code": "KH-01", "category": "programming",
     "tuition_fee": 4000000, "status": "open"},
    {"course_code": "K202", "category": "programming",
     "tuition_fee": 5000000, "status": "full"},
    {"course_code": "K203", "category": "design",
     "tuition_fee": 1500000, "status": "open"}
]


def is_valid_course_code(code):
    """Mã hợp lệ: bắt đầu bằng chữ cái K, theo sau là ít nhất một chữ số (chỉ chữ số)."""
    return len(code) >= 2 and code[0] == "K" and code[1:].isdigit()


def clean_and_validate_courses(raw_list):
    """Yêu cầu 1.1: chuẩn hóa course_code (strip + upper) và loại bỏ khóa học có mã không hợp lệ."""
    cleaned_list = []
    for item in raw_list:
        code = str(item.get("course_code", "")).strip().upper()
        if is_valid_course_code(code):
            cleaned_item = dict(item)  # tạo bản sao, không sửa dữ liệu gốc
            cleaned_item["course_code"] = code
            cleaned_list.append(cleaned_item)
        else:
            print(f"[Loại bỏ] mã khóa học không hợp lệ: {item.get('course_code')!r}")
    return cleaned_list


def search_courses(item_list, max_tuition_fee, status=None):
    """Yêu cầu 1.2: tìm tuyến tính khóa học có tuition_fee <= max_tuition_fee và đúng status (None = bỏ qua status)."""
    result = []
    for item in item_list:
        if item["tuition_fee"] > max_tuition_fee:
            continue
        if status is not None and item["status"] != status:
            continue
        result.append(item)
    return result


def sort_courses_by_tuition_fee_desc(item_list):
    """Yêu cầu 1.3: Bubble Sort giảm dần theo tuition_fee, trả về danh sách mới."""
    sorted_list = list(item_list)
    n = len(sorted_list)
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            if sorted_list[j]["tuition_fee"] < sorted_list[j + 1]["tuition_fee"]:
                sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]
                swapped = True
        if not swapped:
            break
    return sorted_list


def print_courses(title, item_list):
    """In danh sách khóa học dạng bảng để kiểm tra kết quả."""
    print(f"\n===== {title} ({len(item_list)}) =====")
    for item in item_list:
        print(
            f"{item['course_code']:<8} | {item['category']:<14} | "
            f"{item['tuition_fee']:>12,} | {item['status']}"
        )


if __name__ == "__main__":
    valid_courses = clean_and_validate_courses(raw_courses)
    print_courses("1.1 Sau khi chuẩn hóa & validate", valid_courses)

    print_courses(
        "1.2 Tìm khóa học có tuition_fee <= 3000000 và status = 'open'",
        search_courses(valid_courses, 3000000, "open"),
    )
    print_courses(
        "1.2 Tìm khóa học có tuition_fee <= 3000000 (status = None)",
        search_courses(valid_courses, 3000000),
    )

    print_courses("1.3 Sắp xếp tuition_fee giảm dần (Bubble Sort)", sort_courses_by_tuition_fee_desc(valid_courses))
