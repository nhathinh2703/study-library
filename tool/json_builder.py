import json
import os
import config

def save_json_exam(data, out_dir):
    info = {
        "subject": data["subject"],
        "type": data["type"],
        "level": data["level"],
        "commune": data.get("commune"),
        "province": data["province"],
        "year": data["year"],
        "images": data.get("images", []),   # danh sách ảnh nằm trong data
        "drive_upload": data.get("drive_upload"),
        "drive_download": data.get("drive_download"),
        "drive_view": data.get("drive_view"),
        "upload_date": data.get("upload_date"),
        "update_date": data.get("update_date"),
        "caption_page": data.get("caption_page"),
        "caption_profile": data.get("caption_profile"),
        "update_required": False
    }

    json_path = os.path.join(out_dir, "info.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

def save_json_book(data, out_dir):
    info = {
        "id": data.get("id"),
        "title": data.get("title"),
        "author": data.get("author"),
        "category": data.get("category"),
        "pages": data.get("pages"),
        "cover_image": data.get("cover_image"),
        "drive_upload": data.get("drive_upload"),
        "drive_download": data.get("drive_download"),
        "drive_view": data.get("drive_view"),
        "upload_date": data.get("upload_date"),
        "update_date": data.get("update_date"),
        "caption_page": data.get("caption_page"),
        "caption_profile": data.get("caption_profile"),
        "update_required": False
    }
    
    json_path = os.path.join(out_dir, "info.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)

    # Sinh card HTML cho sách
    card_html = f"""
    <div class="card book">
        <span class="badge new">NEW</span>
        <img src="{info['cover_image']}" alt="Bìa sách" class="book-cover">
        <h3>{info['title']}</h3>
        <div class="info-row">
            <span>📖 {info['category']}</span>
            <span>📄 {info.get('pages','')} trang</span>
        </div>
        <div class="info-row">
            <span>✍️ {info['author']}</span>
        </div>
        <div class="info-row">
            <span>📅 {info.get('update_date','')}</span>
        </div>
        <div class="card-actions">
            <a href="{info['drive_view']}" class="btn primary" target="_blank">Xem</a>
            <a href="{info['drive_download']}" class="btn secondary">Tải</a>
        </div>
    </div>
    """

    section_path = os.path.join(config.BOOKS_OUTPUT_DIR, "section_books.txt")
    with open(section_path, "a", encoding="utf-8") as f:
        f.write(card_html)
