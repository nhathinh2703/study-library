import os
import unicodedata
import re

def normalize_filename(text):
    # thay riêng các ký tự đặc biệt trước khi bỏ dấu
    text = text.replace("Đ", "D").replace("đ", "d")

    # bỏ dấu tiếng Việt
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore').decode('utf-8')

    # thay khoảng trắng bằng gạch nối
    text = re.sub(r'\s+', '-', text)

    # bỏ ký tự đặc biệt
    text = re.sub(r'[^A-Za-z0-9\-]', '', text)

    return text
import re

def normalize_location(unit: str) -> str:
    if not unit:
        return ""

    # Tách theo dấu gạch nối
    parts = unit.split("-")
    if len(parts) < 2:
        return unit

    prefix = parts[0]
    rest = " ".join(parts[1:])

    prefix_map = {
        "Tinh": "Tỉnh",
        "ThanhPho": "Thành phố",
        "Truong": "Trường",
        "So": "Sở",
        "Xa": "Xã",
        "Phuong": "Phường",
        "ThiXa": "Thị xã",
        "Huyen": "Huyện",
    }

    prefix_vn = prefix_map.get(prefix, prefix)
    return f"{prefix_vn} {rest}"

# --- parse cho đề thi ---
def parse_exam_filename(filename):
    name, _ = os.path.splitext(filename)
    parts = name.split("_")

    # mẫu: subject_type_level_unit_year
    subject_raw = parts[0]
    exam_type = parts[1]  # lấy trực tiếp, không map
    level = parts[2]
    unit = normalize_location(parts[3])       # có thể là tỉnh, trường, sở...
    year = parts[4] if len(parts) > 4 else ""

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
    return {
        "id": name,
        "subject": subject,
        "type": exam_type,
        "level": level,
        "unit": unit,
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