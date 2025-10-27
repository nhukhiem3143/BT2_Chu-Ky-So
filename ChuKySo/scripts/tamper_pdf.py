# ==========================================
# tamper_pdf_overlay_unicode.py
# Thêm chữ "Xin chào" (có tiếng Việt) vào trang đầu của signed.pdf
# mà không phá chữ ký.
# ==========================================

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pikepdf import Pdf
from pathlib import Path

SIGNED_PDF = "../signed.pdf"
OVERLAY_PDF = "overlay.pdf"
TAMPERED_PDF = "../tampered.pdf"

# === 1. Đăng ký font Unicode ===
# (Chọn một font có hỗ trợ tiếng Việt, ví dụ Arial hoặc DejaVuSans)
FONT_PATH = Path("C:/Windows/Fonts/arial.ttf")  # Đường dẫn font hệ thống
pdfmetrics.registerFont(TTFont("ArialUnicode", str(FONT_PATH)))

# === 2. Tạo overlay có chữ "Xin chào" ===
c = canvas.Canvas(OVERLAY_PDF, pagesize=A4)
c.setFont("ArialUnicode", 14)
c.setFillColorRGB(1, 0, 0)  # đỏ cho dễ thấy
c.drawString(100, 580, "Xin chào, đây là phần đã thêm vào!")
c.save()
print("✅ Đã tạo overlay.pdf")

# === 3. Ghép overlay vào signed.pdf (không phá chữ ký) ===
base = Pdf.open(SIGNED_PDF)
overlay = Pdf.open(OVERLAY_PDF)

page = base.pages[0]
page.add_overlay(overlay.pages[0])

base.save(TAMPERED_PDF)
print(f"💀 Đã thêm 'Xin chào...' vào {TAMPERED_PDF}")
