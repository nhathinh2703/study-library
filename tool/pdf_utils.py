import io
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import fitz  # PyMuPDF
from config import WATERMARK_TEXT

def create_watermark_page(text):
    """Tạo một trang PDF chứa watermark màu tím đậm, giữa trang, hơi mờ"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica-Bold", 28)

    # màu tím đậm hơn (RGB), alpha ~0.2 để hơi mờ
    can.setFillColorRGB(0.4, 0, 0.4, alpha=0.2)

    # vị trí giữa trang
    text_width = can.stringWidth(text, "Helvetica-Bold", 28)
    x = (letter[0] - text_width) / 2
    y = letter[1] / 2

    can.drawString(x, y, text)
    can.save()
    packet.seek(0)
    return PdfReader(packet).pages[0]

def add_pdf_watermark(input_pdf, output_pdf=None, text=WATERMARK_TEXT):
    """Chèn watermark vào tất cả các trang PDF"""
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    watermark_page = create_watermark_page(text)

    for page in reader.pages:
        page.merge_page(watermark_page)
        writer.add_page(page)

    if not output_pdf:
        output_pdf = input_pdf  # ghi đè file gốc

    with open(output_pdf, "wb") as f:
        writer.write(f)

    return output_pdf

def add_pdf_watermark_first_page(input_pdf, output_pdf=None, text=WATERMARK_TEXT):
    """Chèn watermark vào trang đầu tiên của PDF, không duyệt toàn bộ"""
    reader = PdfReader(input_pdf)
    writer = PdfWriter()
    watermark_page = create_watermark_page(text)

    # xử lý trang đầu
    first_page = reader.pages[0]
    first_page.merge_page(watermark_page)
    writer.add_page(first_page)

    # thêm các trang còn lại nguyên xi
    for page in reader.pages[1:]:
        writer.add_page(page)

    if not output_pdf:
        output_pdf = input_pdf  # ghi đè file gốc

    with open(output_pdf, "wb") as f:
        writer.write(f)

    return output_pdf

def extract_cover(pdf_path, cover_path):
    """Xuất ảnh bìa (trang đầu tiên) từ PDF"""
    doc = fitz.open(pdf_path)
    page = doc[0]  # trang đầu
    pix = page.get_pixmap()
    pix.save(cover_path)
    return cover_path