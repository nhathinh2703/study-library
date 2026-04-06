import os, json
import config
from parser import parse_filename
from converter import docx_to_pdf, pdf_to_images
from caption import generate_caption
from json_builder import save_json
from drive_uploader import upload_file, update_file
from pdf_watermark import add_pdf_watermark

processed_count = 0

def get_config(category):
    """Trả về INPUT_DIR, OUTPUT_DIR, DRIVE_INPUT_ID, DRIVE_OUTPUT_ID theo category"""
    if category == "exam":
        return config.EXAMS_INPUT_DIR, config.EXAMS_OUTPUT_DIR, config.DRIVE_EXAMS_INPUT_ID, config.DRIVE_EXAMS_OUTPUT_ID
    elif category == "book":
        return config.BOOKS_DIR, config.BOOKS_DIR, config.DRIVE_BOOKS_ID, config.DRIVE_BOOKS_ID
    elif category == "article":
        return config.ARTICLES_DIR, config.ARTICLES_DIR, config.DRIVE_ARTICLES_ID, config.DRIVE_ARTICLES_ID
    else:
        raise ValueError(f"Unknown category: {category}")

def process_file(file, category, force_update=False):
    global processed_count

    INPUT_DIR, OUTPUT_DIR, DRIVE_INPUT_ID, DRIVE_OUTPUT_ID = get_config(category)

    input_path = os.path.join(INPUT_DIR, file)
    base = file.replace(".docx", "")
    out_dir = os.path.join(OUTPUT_DIR, base)
    json_path = os.path.join(out_dir, "info.json")

    if not os.path.exists(out_dir):
        os.makedirs(out_dir, exist_ok=True)
        print("1) Đã tạo thư mục:", out_dir)
    else:
        print("1) Thư mục đã tồn tại:", out_dir)

    pdf_path = os.path.join(out_dir, base + ".pdf")

    print(f"=== Bắt đầu xử lý: {file} ({category}) ===")

    data = parse_filename(file)
    data["category"] = category  # thêm category vào metadata

    # 2. Convert DOCX -> PDF
    print("2) Đang chuyển DOCX sang PDF...")
    docx_to_pdf(input_path, pdf_path)
    add_pdf_watermark(pdf_path)
    print("   ✓ Đã tạo PDF:", pdf_path)

    # 3. Xuất ảnh từ PDF (xóa ảnh cũ nếu có)
    print("3) Đang chuyển PDF sang ảnh...")
    for f in os.listdir(out_dir):
        if f.endswith(".png"):
            os.remove(os.path.join(out_dir, f))
    images = pdf_to_images(pdf_path, out_dir)
    print(f"   ✓ Đã tạo {len(images)} ảnh")

    # 4. Xử lý ảnh
    print("4) Xử lý ảnh...")
    for idx, img in enumerate(images, start=1):
        print(f"4.{idx}) Đang xử lý ảnh:", img)

    # 5. Upload hoặc update file trên Drive
    docx_link, pdf_link, pdf_download = None, None, None
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            info = json.load(f)
        docx_link = info.get("docx_link")
        pdf_link = info.get("drive_link")
        pdf_download = info.get("pdf_download")

    if force_update:
        print("5) Force update: cập nhật file trên Drive...")
        if docx_link:
            docx_id = docx_link.split("/d/")[1].split("/")[0]
            docx_link = update_file(docx_id, input_path,
                                    mime_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        else:
            docx_link = upload_file(input_path, DRIVE_INPUT_ID)

        if pdf_link:
            pdf_id = pdf_link.split("/d/")[1].split("/")[0]
            pdf_link = update_file(pdf_id, pdf_path, mime_type="application/pdf")
        else:
            pdf_link = upload_file(pdf_path, DRIVE_OUTPUT_ID)

        pdf_id = pdf_link.split("/d/")[1].split("/")[0]
        pdf_download = f"https://drive.google.com/uc?export=download&id={pdf_id}"
        print("   ✓ Đã cập nhật file trên Drive")
    elif not os.path.exists(json_path):
        print("5) Chưa có info.json, upload file mới...")
        docx_link = upload_file(input_path, DRIVE_INPUT_ID)
        print("   ✓ Link DOCX:", docx_link)

        pdf_link = upload_file(pdf_path, DRIVE_OUTPUT_ID)
        print("   ✓ Link PDF xem:", pdf_link)

        pdf_id = pdf_link.split("/d/")[1].split("/")[0]
        pdf_download = f"https://drive.google.com/uc?export=download&id={pdf_id}"
        print("   ✓ Link PDF tải trực tiếp:", pdf_download)
    else:
        print("5) Đã có info.json, tái sử dụng link cũ")

    # 6. Sinh caption
    print("6) Đang tạo caption...")
    title, page, profile = generate_caption(data,
                                            drive_link=pdf_download,
                                            web_link=pdf_link)
    with open(os.path.join(out_dir, "caption_page.txt"), "w", encoding="utf-8") as f:
        f.write(page)
    with open(os.path.join(out_dir, "caption_profile.txt"), "w", encoding="utf-8") as f:
        f.write(profile)
    print("   ✓ Đã lưu caption")

    # 7. Lưu JSON
    print("7) Đang lưu info.json...")
    save_json(data, images, pdf_link, out_dir,
              docx_link=docx_link,
              pdf_download=pdf_download,
              caption_page=page,
              caption_profile=profile)
    print("   ✓ Đã lưu JSON tại:", json_path)

    processed_count += 1
    print(f"=== Hoàn tất xử lý: {file} ===\n")

def main(category="exam"):
    global processed_count
    processed_count = 0

    INPUT_DIR, OUTPUT_DIR, _, _ = get_config(category)

    print("INPUT_DIR =", os.path.abspath(INPUT_DIR))
    print("OUTPUT_DIR =", os.path.abspath(OUTPUT_DIR))

    files = [f for f in os.listdir(INPUT_DIR) if f.endswith(".docx")]
    total = len(files)
    print(f"Tổng số file Word tìm thấy: {total}")

    for idx, file in enumerate(files, start=1):
        base = file.replace(".docx", "")
        out_dir = os.path.join(OUTPUT_DIR, base)
        json_path = os.path.join(out_dir, "info.json")

        print(f"\n=== Đang xử lý file {idx}/{total}: {file} ===")

        if os.path.exists(json_path):
            with open(json_path, "r", encoding="utf-8") as f:
                info = json.load(f)

            if not config.FORCE_UPDATE and not info.get("update_required", False):
                print(f"-> Bỏ qua {file}, đã có info.json và update_required = False")
                continue
            else:
                print(f"-> Chạy lại {file} vì update_required = True hoặc FORCE_UPDATE = True")
                process_file(file, category, force_update=True)

                info["update_required"] = False
                with open(json_path, "w", encoding="utf-8") as f:
                    json.dump(info, f, ensure_ascii=False, indent=2)
        else:
            process_file(file, category, force_update=config.FORCE_UPDATE)

    print("\n=== Hoàn tất ===")
    print(f"Tổng số file đã xử lý (upload/update): {processed_count}")

if __name__ == "__main__":
    # mặc định chạy cho exams, có thể đổi thành "book" hoặc "article"
    main(category="exam")