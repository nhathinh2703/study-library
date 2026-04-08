import os
from datetime import datetime
import unicodedata
import re

def normalize_filename(text):
    # bỏ dấu tiếng Việt
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')
    # thay khoảng trắng bằng gạch nối
    text = re.sub(r'\s+', '-', text)
    # bỏ ký tự đặc biệt
    text = re.sub(r'[^A-Za-z0-9\-]', '', text)
    return text

# --- normalize location (cho đề thi) ---
def normalize_location(name):
    if not name:
        return ""
    name = name.replace("-", " ")
    if name.startswith("Xa"):
        return "Xã " + name[2:]
    elif name.startswith("Phuong"):
        return "Phường " + name[6:]
    elif name.startswith("Tinh"):
        return "Tỉnh " + name[4:]
    return name

# --- parse cho đề thi ---
def parse_exam_filename(filename):
    name, _ = os.path.splitext(filename)
    parts = name.split("_")

    subject_raw = parts[0]
    exam_type_raw = parts[1]
    level = parts[2]
    commune = None
    province = None
    year = None

    if len(parts) == 5:
        province = parts[3]
        year = parts[4]
    elif len(parts) == 6:
        commune = parts[3]
        province = parts[4]
        year = parts[5]

    subject_map = {
        "TinHoc": "Tin học",
        "Toan": "Toán",
        "VatLy": "Vật lý",
        "HoaHoc": "Hóa học",
        "NguVan": "Ngữ văn",
        "TiengAnh": "Tiếng Anh",
        "SinhHoc": "Sinh học",
        "LichSu": "Lịch sử",
        "DiaLy": "Địa lý",
    }
    subject = subject_map.get(subject_raw, subject_raw)

    type_map = {
        "HSG": "Học sinh giỏi",
        "THT": "Tin học trẻ",
        "ChuyenTin10": "Thi vào chuyên Tin lớp 10",
    }
    exam_type = type_map.get(exam_type_raw, exam_type_raw)

    commune = normalize_location(commune) if commune else ""
    province = normalize_location(province) if province else ""
    year = year.replace("-", "–") if year else ""

    return {
        "id": name,
        "subject": subject,
        "type": exam_type,
        "level": level,
        "commune": commune,
        "province": province,
        "year": year
    }

def parse_book_filename(filename):
    """
    Format: Title_Author_Category_Pages.pdf
    """
    name, _ = os.path.splitext(filename)
    parts = name.split("_")

    if len(parts) < 4:
        raise ValueError("Tên file không đúng format: Title_Author_Category_Pages.pdf")

    # giữ nguyên tiếng Việt để hiển thị
    title_vi = parts[0].replace("-", " ")
    author = parts[1].replace("-", " ")
    category = parts[2].replace("-", " ")  # lấy trực tiếp tiếng Việt
    pages = parts[3]

    # tạo thêm tên ASCII để dùng cho file/thư mục
    title_ascii = normalize_filename(title_vi)

    return {
        "id": title_ascii,      # dùng ASCII làm id an toàn
        "title": title_vi,      # hiển thị tiếng Việt
        "title_ascii": title_ascii,
        "author": author,
        "category": category,   # tiếng Việt luôn
        "pages": pages
    }