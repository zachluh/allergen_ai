from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import simpleSplit
import os


def generate(text, pdf_name, title):
    pdf_path = os.path.join('static', pdf_name)
    pdf = Canvas(pdf_path, pagesize=letter)

    # Page size and margins
    page_width, page_height = letter
    left_margin = 50
    right_margin = 50
    top_margin = 720  # Adjusted to leave space for title
    bottom_margin = 50
    line_height = 16  # Space between lines

    pdf.setFont("Helvetica-Bold", 16)  # Title Font
    pdf.drawCentredString(page_width / 2, 770, title)  # Title Position (Centered at top)

    pdf.setFont("Helvetica", 12)  # Reset font for body text

    x = left_margin
    y = top_margin
    max_width = page_width - left_margin - right_margin

    for line in text.split('\n'):
        wrapped_lines = simpleSplit(line, "Helvetica", 12, max_width)  # Auto-wrap text
        for subline in wrapped_lines:
            if y < bottom_margin:  # If text reaches bottom margin, create a new page
                pdf.showPage()
                pdf.setFont("Helvetica-Bold", 16)
                pdf.drawCentredString(page_width / 2, 770, title)  # Re-add title on new page
                pdf.setFont("Helvetica", 12)
                y = top_margin  # Reset Y position for new page

            pdf.drawString(x, y, subline)
            y -= line_height  # Move cursor down

    pdf.save()
