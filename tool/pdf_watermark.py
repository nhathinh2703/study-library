from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import io
from config import WATERMARK_TEXT

import io
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

import io
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

import io
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

def create_watermark_page(text):
    """Tạo một trang PDF chứa watermark màu tím, góc phải sát đáy, mờ"""
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica-Bold", 20)

    # màu tím nhạt (RGB), alpha ~0.3 để mờ
    can.setFillColorRGB(0.5, 0, 0.5, alpha=0.3)

    # vị trí góc phải dưới (cách mép phải 0.5 inch, mép dưới 0.3 inch)
    text_width = can.stringWidth(text, "Helvetica-Bold", 20)
    x = letter[0] - text_width - 0.5 * inch
    y = 0.3 * inch

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

    print(f"   ✓ Đã chèn watermark vào PDF: {output_pdf}")
    return output_pdf