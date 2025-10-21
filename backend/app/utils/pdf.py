from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

def build_receipt_pdf(data: dict) -> bytes:
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    width, height = A4
    y = height - 20*mm
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20*mm, y, "Grievance / Feedback Receipt")
    y -= 10*mm
    c.setFont("Helvetica", 11)
    lines = [
        f"Grievance ID: {data.get('id')}",
        f"Created at: {data.get('created_at')}",
        f"Anonymous: {data.get('is_anonymous')}",
        f"Details: {data.get('details') or '-'}",
        f"Category type: {data.get('category_type') or '-'}",
    ]
    for line in lines:
        c.drawString(20*mm, y, line)
        y -= 7*mm
    c.showPage()
    c.save()
    pdf = buf.getvalue()
    buf.close()
    return pdf
