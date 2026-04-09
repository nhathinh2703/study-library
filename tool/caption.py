from config import GITHUB_PAGE_URL

def generate_exam_caption(data, web_link=GITHUB_PAGE_URL):
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

    # exam_type lấy trực tiếp
    exam_type = data.get("type", "")

    # title: chỉ còn unit (tỉnh, trường, sở...)
    title = f"ĐỀ THI {exam_type} MÔN {subject} CẤP {data['level']}, {data['unit']}, năm {data['year']}"

    drive_download = data.get("drive_download", "")
    drive_view = data.get("drive_view", "")

    # caption cho page
    page = f"""💻 ĐỀ THI {exam_type.upper()} MÔN {subject.upper()} CẤP {data['level']}

📍 {data['unit']} | 🎯 {data['year']}

📥 Tải PDF:
👉 {drive_download}

📖 Xem PDF trực tuyến:
👉 {drive_view}

🌐 Trang web tổng hợp đầy đủ các đề:
👉 {web_link}

✨ Chúc các bạn rèn luyện đạt hiệu quả cao và tự tin bước vào kỳ thi! ✨
"""

    # caption cho profile
    profile = f"""Mình vừa tổng hợp đề này 👇

💻 {title.upper()}

📥 Tải PDF:
👉 {drive_download}

📖 Xem PDF trực tuyến:
👉 {drive_view}

🌐 Trang web tổng hợp đầy đủ các đề:
👉 {web_link}

✨ Chúc các bạn học tập tốt và đạt kết quả như mong muốn! ✨
"""

    return title, page, profile

def generate_book_caption(data, web_link=GITHUB_PAGE_URL):
    title = data.get("title", "")
    author = data.get("author", "")
    pages = data.get("pages", "")
    drive_upload = data.get("drive_upload", "")
    drive_download = data.get("drive_download", "")
    drive_view = data.get("drive_view", "")

    # caption cho page
    caption_page = f"""📚 SÁCH: {title.upper()}

✍️ Tác giả: {author}
📖 Số trang: {pages}

📥 Tải PDF:
👉 {drive_download}

📖 Xem PDF trực tuyến:
👉 {drive_view}

🌐 Thư viện tổng hợp:
👉 {web_link}

✨ Chúc bạn đọc sách hiệu quả và bổ ích! ✨
"""

    # caption cho profile
    caption_profile = f"""Mình vừa thêm sách mới 👇

📚 {title} - {author} ({pages} trang)

📥 Tải PDF:
👉 {drive_download}

📖 Xem PDF trực tuyến:
👉 {drive_view}

🌐 Trang web tổng hợp đầy đủ các sách:
👉 {web_link}
"""

    return title, caption_page, caption_profile
