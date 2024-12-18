from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import letter
import os

def generate(text, pdf_name):
    pdf = Canvas(os.path.join('static', pdf_name))

    pdfText = pdf.beginText(50, 750)
    pdfText.setTextOrigin(50, 750)
    pdfText.setFont("Helvetica", 12)

    for line in text.split('\n'):
        pdfText.textLines(line)

    pdf.drawText(pdfText)

    pdf.save()
