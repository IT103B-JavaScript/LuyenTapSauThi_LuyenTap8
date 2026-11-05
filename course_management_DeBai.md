# ĐÁNH GIÁ CHẤT LƯỢNG KỸ NĂNG – PYTHON, FASTAPI VÀ DATABASE
## KIỂM TRA ĐÁNH GIÁ NĂNG LỰC CNTT – [Mã đề: 010]
**THỜI GIAN: 90 phút**

---

## Yêu cầu
Tạo project folder theo hướng dẫn sau:
- Tạo folder [Mã Lớp]\_[Họ Tên]\_[Mã Đề] chứa toàn bộ file mã nguồn. *Ví dụ: HN_KS25_CNTT1_NguyenVanA_10*
- Sau khi hoàn thành project, đẩy code lên GitHub và nộp link cho người phụ trách.
- Công nghệ & công cụ sử dụng: Python core + FastAPI + MySQL + SQLAlchemy ORM, Visual Studio Code.

## Thực hành

### 1. Bối cảnh
Hệ thống Quản lý Khóa học trực tuyến (course_management) cần xây dựng các chức năng xử lý dữ liệu khóa học bằng Python Core, cấu hình dữ liệu đầu vào/đầu ra với Pydantic, kết nối cơ sở dữ liệu MySQL và viết các API quản lý khóa học (courses) và danh mục khóa học (course_categories).

Sinh viên cần xây dựng API quản lý khóa học, cho phép thêm mới khóa học, xem danh sách khóa học kèm chi tiết danh mục khóa học, và xóa danh mục khóa học kèm xử lý ràng buộc đặc biệt.

### 2. Tài liệu

#### 2.1 Dữ liệu khóa học (dùng cho Phần 1)
Cho trước danh sách dữ liệu thô chứa thông tin các khóa học giả định sau:
```python
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
```

#### 2.2 Cơ sở dữ liệu
Database đặt tên là: **course_db**

**Bảng course_categories:**
| Trường | Kiểu dữ liệu | Mô tả |
|---|---|---|
| **id** | int | Mã danh mục khóa học, khóa chính, tự tăng |
| **name** | string | Tên danh mục khóa học, tối đa 50 ký tự, độc nhất, không trống |

**Bảng courses:**
| Trường | Kiểu dữ liệu | Mô tả |
|---|---|---|
| **id** | int | Mã định danh khóa học, khóa chính, tự tăng |
| **course_code** | string | Mã khóa học, tối đa 10 ký tự, độc nhất, không trống |
| **tuition_fee** | float | Học phí, không trống |
| **course_category_id** | int | Khóa ngoại liên kết tới bảng course_categories |

#### 2.3 Bảng danh sách API
| STT | Chức năng | Method | Endpoint |
|---|---|---|---|
| 1 | Truy vấn danh sách khóa học | GET | /courses |
| 2 | Thêm khóa học mới | POST | /courses |
| 3 | Xóa danh mục khóa học | DELETE | /course-categories/{id} |

#### 2.4 Quy chuẩn cấu trúc Response chung
Tất cả các API bắt buộc phải trả về dữ liệu dưới dạng đồng nhất gồm 4 trường sau:
- **statusCode** (số nguyên): mã trạng thái HTTP (200, 201, 404, ...).
- **error** (chuỗi hoặc null): lỗi nếu có (ví dụ: "Not Found").
- **message** (chuỗi): thông báo trạng thái thực hiện hành động cho người dùng.
- **data** (object/mảng hoặc null): dữ liệu kết quả trả về từ database.

**Ví dụ mẫu Response API lấy danh sách khóa học thành công:**
```json
{
  "statusCode": 200,
  "error": null,
  "message": "Lấy danh sách khóa học thành công",
  "data": [
    {
      "id": 1,
      "course_code": "K101",
      "tuition_fee": 3500000.0,
      "course_category": {
        "id": 1,
        "name": "programming"
      }
    }
  ]
}
```

### 3. Yêu cầu nghiệp vụ

#### Phần 1: Python Core & Tư duy thuật toán (35 điểm)
**Yêu cầu 1.1 (10 điểm) – Chuẩn hóa & validate dữ liệu:**
Viết hàm `clean_and_validate_courses` thực hiện:
- Loại bỏ khoảng trắng thừa ở hai đầu của mã khóa học `course_code` và chuyển toàn bộ chữ cái thành dạng in hoa (ví dụ: " k102 " → "K102").
- Kiểm tra tính hợp lệ của mã khóa học sau khi chuẩn hóa: phải bắt đầu bằng chữ cái K, theo sau là các chữ số. Nếu không hợp lệ, loại bỏ khóa học đó khỏi danh sách.

**Yêu cầu 1.2 (12 điểm) – Tìm kiếm tuyến tính (Linear Search):**
Viết hàm `search_courses` để tìm kiếm các khóa học thỏa mãn đồng thời:
- Học phí (`tuition_fee`) nhỏ hơn hoặc bằng giá trị truyền vào tham số.
- Trạng thái (`status`) trùng khớp với giá trị truyền vào tham số (nếu giá trị truyền vào là None thì chỉ lọc theo học phí).

**Yêu cầu 1.3 (13 điểm) – Sắp xếp nổi bọt (Bubble Sort):**
Viết hàm `sort_courses_by_tuition_fee_desc` tự cài đặt thuật toán Bubble Sort để sắp xếp danh sách khóa học theo thứ tự học phí giảm dần.

#### Phần 2: Parameter & Pydantic Validation (10 điểm)
**Yêu cầu 2.1 (5 điểm) – Định nghĩa Schema & validate dữ liệu:**
Tạo Schema `CourseCreate` để validate dữ liệu đầu vào:
- `course_code`: bắt buộc, độ dài tối thiểu 4 ký tự, tối đa 10 ký tự.
- `tuition_fee`: bắt buộc, giá trị phải lớn hơn 0.
- `course_category_id`: bắt buộc (ID liên kết với bảng danh mục khóa học).

**Yêu cầu 2.2 (5 điểm) – Phản hồi chuẩn RESTful & Response Model:**
Tạo Schema `CourseResponse` dùng làm response_model khi trả về thông tin khóa học.

#### Phần 3: Kết nối MySQL & SQLAlchemy ORM (20 điểm)
**Yêu cầu 3.1 (10 điểm) – Khai báo cấu hình CSDL:**
Viết file `database.py` kết nối tới cơ sở dữ liệu MySQL local có tên course_db.

**Yêu cầu 3.2 (10 điểm) – Thiết kế Model quan hệ 1-N:**
Khai báo 2 SQLAlchemy Models trong thư mục `models/` đại diện cho mối quan hệ 1-N:
- Bảng course_categories: tạo các cột tương ứng, thiết lập mối quan hệ.
- Bảng courses: tạo các cột tương ứng, thiết lập mối quan hệ.

#### Phần 4: Endpoints API & logic nghiệp vụ (35 điểm)
**Yêu cầu 4.1 (5 điểm) – Chia thư mục/file:** Chia thư mục/file theo cấu trúc phân tầng nêu ở mục 5. Yêu cầu kỹ thuật.

**Yêu cầu 4.2 (10 điểm) – API 1: POST /courses**
- **Mô tả:** thêm mới một khóa học.
- **Yêu cầu:** thêm dữ liệu khóa học từ Request Body vào database; xử lý trường hợp `course_category_id` không tồn tại và `course_code` bị trùng.

**Yêu cầu 4.3 (10 điểm) – API 2: GET /courses**
- **Mô tả:** truy vấn danh sách khóa học.
- **Yêu cầu:** trả về danh sách khóa học kèm theo thông tin chi tiết của danh mục khóa học đó.

**Yêu cầu 4.4 (10 điểm) – API 3: DELETE /course-categories/{id}**
- **Mô tả:** xóa danh mục khóa học theo ID.
- **Yêu cầu:** chỉ cho phép xóa khi không có khóa học nào thuộc danh mục khóa học này.

### 4. Thang điểm chi tiết
| STT | Nghiệp vụ cần đạt được | Mô tả chi tiết nghiệp vụ | Điểm |
|---|---|---|---|
| 1 | Phần 1 – Python Core & Tư duy thuật toán | Yêu cầu 1.1 – Chuẩn hóa & validate dữ liệu: 10 • Yêu cầu 1.2 – Tìm kiếm tuyến tính: 12 • Yêu cầu 1.3 – Sắp xếp nổi bọt: 13 | 35 |
| 2 | Phần 2 – Parameter & Pydantic Validation | Yêu cầu 2.1 – Schema CourseCreate & validate dữ liệu: 5 • Yêu cầu 2.2 – Schema CourseResponse & response_model: 5 | 10 |
| 3 | Phần 3 – Kết nối MySQL & SQLAlchemy ORM | Yêu cầu 3.1 – Cấu hình kết nối CSDL (database.py): 10 • Yêu cầu 3.2 – Model quan hệ 1-N: 10 | 20 |
| 4 | Phần 4 – Endpoints API & logic nghiệp vụ | Yêu cầu 4.1 – Chia thư mục/file: 5 • Yêu cầu 4.2 – API POST /courses: 10 • Yêu cầu 4.3 – API GET /courses: 10 • Yêu cầu 4.4 – API DELETE /course-categories/{id}: 10 | 35 |
| | **Tổng cộng** | | **100** |

### 5. Yêu cầu kỹ thuật
- Chạy được chương trình bằng lệnh `uvicorn main:app --reload`.
- Test được API trên Swagger UI.
- Kết nối được FastAPI với MySQL thông qua SQLAlchemy ORM.
- Source code được tách thành nhiều file theo cấu trúc phân tầng rõ ràng và hợp lý.

*Lưu ý: Chỉ tính điểm khi chức năng chương trình thực hiện đúng theo yêu cầu nghiệp vụ được giao.*

---

## Hướng dẫn chạy bài giải mẫu (thư mục `course_management/`)
```
course_management/
├── main.py                     # khởi tạo app, đăng ký router, xử lý lỗi
├── database.py                 # kết nối MySQL course_db
├── models/
│   ├── __init__.py
│   ├── course_category.py
│   └── course.py
├── schemas/
│   ├── __init__.py
│   └── course_schema.py
├── services/
│   ├── __init__.py
│   ├── course_service.py
│   └── course_category_service.py
├── routers/
│   ├── __init__.py
│   ├── course_router.py
│   └── course_category_router.py
├── utils/
│   ├── __init__.py
│   ├── python_core.py          # Phần 1
│   ├── exceptions.py
│   └── response.py
├── create_database.sql
└── requirements.txt
```
1. `pip install -r requirements.txt`
2. Chạy `create_database.sql` trong MySQL (tạo database `course_db`), sửa user/mật khẩu trong `database.py` nếu khác `root/123456`.
3. Phần 1: `python -m utils.python_core`
4. API: `uvicorn main:app --reload` → mở http://127.0.0.1:8000/docs. Khi khởi động, bảng `course_categories` được tạo sẵn các loại: 1 = programming, 2 = design, 3 = marketing.
