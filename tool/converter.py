import os
from docx2pdf import convert
from pdf2image import convert_from_path
from config import DPI

# Đường dẫn tới thư mục bin của Poppler
POPPLER_PATH = r"C:\poppler-25.12.0\Library\bin"

def docx_to_pdf(input_path, output_pdf):
    convert(input_path, output_pdf)

def pdf_to_images(pdf_path, output_folder):
    # Truyền thêm poppler_path để chắc chắn pdf2image tìm đúng
    images = convert_from_path(pdf_path, dpi=DPI, poppler_path=POPPLER_PATH)

    paths = []
    for i, img in enumerate(images):
        img_path = os.path.join(output_folder, f"page_{i+1}.png")
        img.save(img_path, "PNG")
        paths.append(img_path)

    return paths