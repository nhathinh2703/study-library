from config import GITHUB_PAGE_URL

def generate_caption(data, web_link=GITHUB_PAGE_URL):
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
    subject = subject_map.get(data.get("subject"), data.get("subject"))

    # mapping type
    type_map = {
        "HSG": "Học sinh giỏi",
        "THT": "Tin học trẻ",
        "ChuyenTin10": "Thi vào chuyên Tin lớp 10",
    }
    exam_type = type_map.get(data.get("type"), data.get("type"))

    # title: nếu có xã/phường thì thêm vào, nếu không thì chỉ tỉnh
    if data.get("commune"):
        title = f"Đề {exam_type} {subject} {data['level']} {data['commune']}, {data['province']} {data['year']}"
    else:
        title = f"Đề {exam_type} {subject} {data['level']} {data['province']} {data['year']}"

    # caption cho page
    page = f"""💻 ĐỀ THI {exam_type.upper()} {subject.upper()} {data['level']}

📍 {data['province']}{' - ' + data['commune'] if data.get('commune') else ''} | 🎯 {data['year']}

📥 Tải PDF:
👉 {data.get("pdf_download")}

📖 Xem PDF trực tuyến:
👉 {data.get("drive_link")}

🌐 Trang web tổng hợp đầy đủ các đề:
👉 {web_link}

✨ Chúc các bạn rèn luyện đạt hiệu quả cao và tự tin bước vào kỳ thi! ✨
"""

    # caption cho profile
    profile = f"""Mình vừa tổng hợp đề này 👇

💻 {title.upper()}

📥 Tải PDF:
👉 {data.get("drive_link")}

📖 Xem PDF trực tuyến:
👉 {data.get("drive_link")}

🌐 Trang web tổng hợp đầy đủ các đề:
👉 {web_link}

✨ Chúc các bạn học tập tốt và đạt kết quả như mong muốn! ✨
"""

    return title, page, profile