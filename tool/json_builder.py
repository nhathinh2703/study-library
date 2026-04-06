import json
import os

def save_json(data, images, pdf_link, out_dir,
              docx_link=None,
              pdf_download=None,
              caption_page=None,
              caption_profile=None):
    info = {
        "subject": data["subject"],
        "type": data["type"],
        "level": data["level"],
        "commune": data.get("commune"),
        "province": data["province"],
        "year": data["year"],
        "images": images,             # danh sách ảnh
        "drive_link": pdf_link,       # link xem PDF
        "pdf_download": pdf_download, # link tải trực tiếp PDF
        "docx_link": docx_link,       # link DOCX
        "caption_page": caption_page,       # caption cho page
        "caption_profile": caption_profile, # caption cho profile
        "update_required": False      # mặc định
    }
    json_path = os.path.join(out_dir, "info.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)