import os

def normalize_location(name):
    if not name:
        return ""
    name = name.replace("-", " ")
    if name.startswith("Xa"):
        return "xã " + name[2:]
    elif name.startswith("Phuong"):
        return "phường " + name[6:]
    elif name.startswith("Tinh"):
        return "tỉnh " + name[4:]
    return name

def parse_filename(filename):
    # bỏ phần mở rộng .docx
    name, _ = os.path.splitext(filename)

    # tách theo dấu "_"
    parts = name.split("_")

    subject_raw = parts[0]       # TinHoc
    exam_type_raw = parts[1]     # HSG, THT, ChuyenTin10...
    level = parts[2]             # THCS, THPT...
    commune = None
    province = None
    year = None

    # nếu có 5 phần trở lên thì có commune
    if len(parts) == 5:
        province = parts[3]
        year = parts[4]
    elif len(parts) == 6:
        commune = parts[3]
        province = parts[4]
        year = parts[5]

    # mapping subject
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

    # mapping type
    type_map = {
        "HSG": "Học sinh giỏi",
        "THT": "Tin học trẻ",
        "ChuyenTin10": "Thi vào chuyên Tin lớp 10",
    }
    exam_type = type_map.get(exam_type_raw, exam_type_raw)

    # chuẩn hóa location
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