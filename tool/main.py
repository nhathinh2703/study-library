import os, json
import config
import shutil
from datetime import datetime
from parser import parse_book_filename, parse_exam_filename, normalize_filename
from converter import docx_to_pdf, pdf_to_images
from caption import generate_exam_caption, generate_book_caption
from json_builder import save_json_exam, save_json_book
from drive_uploader import upload_file, update_file
from pdf_utils import add_pdf_watermark, extract_cover, add_pdf_watermark_first_page
from generate_html import generate_html, generate_index_html

processed_count = 0

def init_section_books():
    section_path = os.path.join(config.BOOKS_OUTPUT_DIR, "section_books.txt")
    with open(section_path, "w", encoding="utf-8") as f:
        f.write("""        <section class="hero">
            <h1>Học liệu</h1>
            <p class="subtitle">Kho sách và tài liệu tham khảo cho học sinh.</p>
        </section>
        <section id="books">
            <div class="card-container">""")
    return section_path

def finalize_section_books():
    section_path = os.path.join(config.BOOKS_OUTPUT_DIR, "section_books.txt")
    with open(section_path, "a", encoding="utf-8") as f:
        f.write("""    </div>
    <div class="pagination">
        <button>« Trước</button>
        <span>Trang 1/1</span>
        <button>Sau »</button>
    </div>
</section>
""")

def init_section_exams():
    section_path = os.path.join(config.EXAMS_OUTPUT_DIR, "section_exams.txt")
    with open(section_path, "w", encoding="utf-8") as f:
        f.write("""        <section class="hero">
            <h1>Đề thi</h1>
            <p class="subtitle">Kho đề thi Tin học các kỳ, nhiều năm học và tỉnh thành để tham khảo và luyện tập.</p>
        </section>
        <section id="exams">
            <div class="card-container">""")
    return section_path

def finalize_section_exams():
    section_path = os.path.join(config.EXAMS_OUTPUT_DIR, "section_exams.txt")
    with open(section_path, "a", encoding="utf-8") as f:
        f.write("""    </div>
    <div class="pagination">
        <button>« Trước</button>
        <span>Trang 1/1</span>
        <button>Sau »</button>
    </div>
</section>
""")

def get_config(category):
    """Trả về INPUT_DIR, OUTPUT_DIR, DRIVE_INPUT_ID, DRIVE_OUTPUT_ID theo category"""
    if category == "exam":
        return config.EXAMS_INPUT_DIR, config.EXAMS_OUTPUT_DIR, config.DRIVE_EXAMS_INPUT_ID, config.DRIVE_EXAMS_OUTPUT_ID
    elif category == "book":
        return config.BOOKS_INPUT_DIR, config.BOOKS_OUTPUT_DIR, config.DRIVE_BOOKS_INPUT_ID, config.DRIVE_BOOKS_OUTPUT_ID
    elif category == "article":
        return config.ARTICLES_DIR, config.ARTICLES_DIR, config.DRIVE_ARTICLES_ID, config.DRIVE_ARTICLES_ID
    else:
        raise ValueError(f"Unknown category: {category}")

def process_exams(file, force_update=False):
    global processed_count

    INPUT_DIR, OUTPUT_DIR, DRIVE_INPUT_ID, DRIVE_OUTPUT_ID = get_config("exam")

    input_path = os.path.join(INPUT_DIR, file)
    base = file.replace(".docx", "")
    out_dir = os.path.join(OUTPUT_DIR, base)
    json_path = os.path.join(out_dir, "info.json")

    print(f"\n=== Xử lý EXAM: {file} ===".upper())

    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
    print("→ Bước 1: Tạo thư mục:", out_dir)    

    pdf_path = os.path.join(out_dir, base + ".pdf")

    # 1. Parse metadata
    data = parse_exam_filename(file)

    # 2. Convert DOCX -> PDF + watermark
    print("→ Bước 2: Chuyển DOCX sang PDF...")
    docx_to_pdf(input_path, pdf_path)
    add_pdf_watermark(pdf_path)

    # 3. Xuất ảnh từ PDF
    print("→ Bước 3: Xuất ảnh từ PDF...")
    for f in os.listdir(out_dir):
        if f.endswith(".png"):
            os.remove(os.path.join(out_dir, f))
    data["images"] = pdf_to_images(pdf_path, out_dir)

    # 4. Upload hoặc update file trên Drive
    print("→ Bước 4: Upload/Update Drive...")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            info = json.load(f)
        data["drive_upload"] = info.get("drive_upload")
        data["drive_download"] = info.get("drive_download")
        data["drive_view"] = info.get("drive_view")
        data["upload_date"] = info.get("upload_date")

    if force_update or not os.path.exists(json_path):
        # upload file gốc (DOCX)
        if data.get("drive_upload"):
            drive_upload_id = data["drive_upload"].split("/d/")[1].split("/")[0]
            data["drive_upload"] = update_file(drive_upload_id, input_path,
                                    mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        else:
            data["drive_upload"] = upload_file(input_path, DRIVE_INPUT_ID)
            data["upload_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # upload file PDF (watermark)
        if data.get("drive_view"):
            drive_view_id = data["drive_view"].split("/d/")[1].split("/")[0]
            data["drive_view"] = update_file(drive_view_id, pdf_path, mime_type="application/pdf")
        else:
            data["drive_view"] = upload_file(pdf_path, DRIVE_OUTPUT_ID)

        drive_view_id = data["drive_view"].split("/d/")[1].split("/")[0]
        data["drive_download"] = f"https://drive.google.com/uc?export=download&id={drive_view_id}"

    # 5. Sinh caption
    print("→ Bước 5: Sinh caption...")
    _, page, profile = generate_exam_caption(data, web_link=config.GITHUB_PAGE_URL)
    data["caption_page"] = page
    data["caption_profile"] = profile
    with open(os.path.join(out_dir, "caption_page.txt"), "w", encoding="utf-8") as f:
        f.write(page)
    with open(os.path.join(out_dir, "caption_profile.txt"), "w", encoding="utf-8") as f:
        f.write(profile)

    # 6. Lưu JSON
    print("→ Bước 6: Lưu info.json...")
    data["update_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_json_exam(data, out_dir)

    processed_count += 1
    print(f"✓ Hoàn tất: {file}\n")

def process_books(file, force_update=False):
    global processed_count

    INPUT_DIR, OUTPUT_DIR, DRIVE_INPUT_ID, DRIVE_OUTPUT_ID = get_config("book")

    input_path = os.path.join(INPUT_DIR, file)

    # 1. Parse metadata trước
    data = parse_book_filename(file)

    # Tạo tên thư mục đầy đủ nhưng ASCII (bỏ dấu)
    folder_name = f"{data['title_ascii']}_{normalize_filename(data['author'])}_{normalize_filename(data['category'])}_{data['pages']}"
    out_dir = os.path.join(OUTPUT_DIR, folder_name)
    json_path = os.path.join(out_dir, "info.json")
    os.makedirs(out_dir, exist_ok=True)

    print(f"\n=== Xử lý book: {file} ===".upper())
    print("→ Bước 1: Tạo thư mục:", out_dir)

    # File PDF giữ nguyên tên gốc
    base = os.path.splitext(file)[0]
    pdf_path = os.path.join(out_dir, base + ".pdf")

    # 2. Copy PDF gốc + watermark
    print("→ Bước 2: Copy PDF và thêm watermark (trang đầu)...")
    shutil.copy(input_path, pdf_path)
    add_pdf_watermark_first_page(pdf_path)

    # 3. Xuất ảnh bìa từ PDF (trang đầu) theo id ASCII
    print("→ Bước 3: Tạo ảnh bìa từ PDF...")
    cover_name = f"cover_{data['id']}.jpg"
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    cover_dir = os.path.join(repo_root, "docs", "assets", "images")
    os.makedirs(cover_dir, exist_ok=True)
    cover_path = os.path.join(cover_dir, cover_name)
    extract_cover(pdf_path, cover_path)
    data["cover_image"] = os.path.relpath(cover_path, os.path.join(repo_root, "docs"))

    # 4. Upload hoặc update file trên Drive
    print("→ Bước 4: Upload/Update Drive...")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            info = json.load(f)
        data["drive_upload"] = info.get("drive_upload")
        data["drive_download"] = info.get("drive_download")
        data["drive_view"] = info.get("drive_view")
        data["upload_date"] = info.get("upload_date")

    if force_update or not os.path.exists(json_path):
        # upload file gốc (input PDF)
        if data.get("drive_upload"):
            drive_upload_id = data["drive_upload"].split("/d/")[1].split("/")[0]
            data["drive_upload"] = update_file(drive_upload_id, input_path, mime_type="application/pdf")
        else:
            data["drive_upload"] = upload_file(input_path, DRIVE_INPUT_ID)
            data["upload_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # upload file đã xử lý (watermark)
        if data.get("drive_view"):
            drive_view_id = data["drive_view"].split("/d/")[1].split("/")[0]
            data["drive_view"] = update_file(drive_view_id, pdf_path, mime_type="application/pdf")
        else:
            data["drive_view"] = upload_file(pdf_path, DRIVE_OUTPUT_ID)

        drive_view_id = data["drive_view"].split("/d/")[1].split("/")[0]
        data["drive_download"] = f"https://drive.google.com/uc?export=download&id={drive_view_id}"

    # 5. Sinh caption
    print("→ Bước 5: Sinh caption...")
    _, page, profile = generate_book_caption(data, web_link=config.GITHUB_PAGE_URL)
    data["caption_page"] = page
    data["caption_profile"] = profile
    with open(os.path.join(out_dir, "caption_page.txt"), "w", encoding="utf-8") as f:
        f.write(page)
    with open(os.path.join(out_dir, "caption_profile.txt"), "w", encoding="utf-8") as f:
        f.write(profile)

    # 6. Lưu JSON
    print("→ Bước 6: Lưu info.json và sinh html...")
    data["update_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_json_book(data, out_dir=out_dir)

    processed_count += 1
    print(f"✓ Hoàn tất book: {file}\n")

def main():
    global processed_count
    processed_count = 0

    # khởi tạo section_exams.txt mới
    init_section_exams()

    # khởi tạo section_books.txt mới
    init_section_books()

    # xử lý exams
    INPUT_DIR, OUTPUT_DIR, _, _ = get_config("exam")
    exam_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".docx")]
    for file in exam_files:
        process_exams(file, force_update=config.FORCE_UPDATE)

    # xử lý books
    INPUT_DIR, OUTPUT_DIR, _, _ = get_config("book")
    book_files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".pdf")]
    for file in book_files:
        process_books(file, force_update=config.FORCE_UPDATE)

    # đóng section_exams.txt
    finalize_section_exams()

    # đóng section_books.txt
    finalize_section_books()

    print("\n=== Hoàn tất xử lý dữ liệu ===")
    print(f"Tổng số file đã xử lý: {processed_count}")

    # hỏi người dùng có muốn sinh HTML không
    choice = input("\nBạn có muốn sinh các trang HTML (index, exam, book)? [y/n]: ").strip().lower()
    if choice == "y":
        generate_index_html()
        generate_html("exam.html", "Thư viện học tập - Đề thi", section_file=config.SECTION_EXAM_FILE)
        generate_html("book.html", "Thư viện học tập - Học liệu", section_file=config.SECTION_BOOK_FILE)
        print("\n=== Đã sinh các trang HTML trong thư mục docs ===")
    else:
        print("Bỏ qua bước sinh HTML.")

if __name__ == "__main__":
    main()