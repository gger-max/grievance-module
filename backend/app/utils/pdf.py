from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from datetime import datetime
from typing import List, Dict, Any
import os
from pathlib import Path

def format_timestamp(iso_string: str) -> str:
    """Convert ISO timestamp to local time format like 'Tue Jul 22 2025 18:06:48'"""
    try:
        dt = datetime.fromisoformat(iso_string.replace('Z', '+00:00'))
        # Convert to local time
        local_dt = dt.astimezone()
        # Format as: Tue Jul 22 2025 18:06:48
        return local_dt.strftime("%a %b %d %Y %H:%M:%S")
    except Exception:
        return iso_string

def build_receipt_pdf(data: dict) -> bytes:
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)
    
    # Set PDF metadata - this sets the browser tab title
    grievance_id = data.get('id', 'Receipt')
    c.setTitle(grievance_id)
    c.setAuthor("Vaka Sosiale Grievance System")
    c.setSubject(f"Grievance Receipt - {grievance_id}")
    
    width, height = A4
    y = height - 20*mm
    
    # Add logo image at the top (centered)
    logo_path = Path(__file__).parent.parent / "static" / "images" / "VAKA SOCIALE_final_NEW.png"
    if logo_path.exists():
        try:
            # Load and draw the logo
            img = ImageReader(str(logo_path))
            img_width = 50*mm  # Logo width
            img_height = 15*mm  # Logo height
            x_logo = (width - img_width) / 2  # Center the logo
            c.drawImage(img, x_logo, y - img_height, width=img_width, height=img_height, preserveAspectRatio=True, mask='auto')
            y -= (img_height + 5*mm)  # Move down after logo
        except Exception as e:
            # If logo fails to load, just skip it
            pass
    
    c.setFont("Helvetica-Bold", 16)
    
    # Center-align the title
    title = "Grievance / Feedback Receipt"
    title_width = c.stringWidth(title, "Helvetica-Bold", 16)
    x_centered = (width - title_width) / 2
    c.drawString(x_centered, y, title)
    
    y -= 15*mm
    
    # Format created_at timestamp
    created_at_formatted = format_timestamp(data.get('created_at', ''))
    
    # Format anonymous field as Yes/No
    is_anonymous = data.get('is_anonymous')
    anonymous_text = "Yes" if is_anonymous else "No"
    
    # Prepare table data
    table_data = []
    
    # Basic information
    table_data.append(["Grievance ID:", data.get('id', '')])
    table_data.append(["Created at:", created_at_formatted])
    table_data.append(["Anonymous:", anonymous_text])
    
    # Add complainant information if not anonymous
    if not is_anonymous:
        if data.get('complainant_name'):
            table_data.append(["Name:", data.get('complainant_name')])
        
        if data.get('complainant_email'):
            table_data.append(["Email:", data.get('complainant_email')])
        
        if data.get('complainant_phone'):
            table_data.append(["Phone:", data.get('complainant_phone')])
        
        if data.get('complainant_gender'):
            table_data.append(["Gender:", data.get('complainant_gender')])
        
        if data.get('hh_id'):
            table_data.append(["Household ID:", data.get('hh_id')])
        
        if data.get('hh_address'):
            table_data.append(["Landmark:", data.get('hh_address')])
    
    # Add details and category
    table_data.append(["Details:", data.get('details') or '-'])
    table_data.append(["Category type:", data.get('category_type') or '-'])
    
    # Create styles for table cells
    styles = getSampleStyleSheet()
    
    # Bold style for labels (first column)
    label_style = ParagraphStyle(
        'Label',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
    )
    
    # Italic style for content (second column)
    content_style = ParagraphStyle(
        'Content',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=11,
        leading=14,
    )
    
    # Convert table data to use Paragraph objects for proper text wrapping
    formatted_table_data = []
    for row in table_data:
        formatted_table_data.append([
            Paragraph(row[0], label_style),
            Paragraph(str(row[1]), content_style)
        ])
    
    # Create the table
    col_widths = [45*mm, 125*mm]  # Column widths
    table = Table(formatted_table_data, colWidths=col_widths)
    
    # Apply table style
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    
    # Calculate table height and draw it
    table_width, table_height = table.wrap(width, height)
    table.drawOn(c, 20*mm, y - table_height)
    
    y -= (table_height + 10*mm)
    
    # Add attachments if present
    attachments = data.get('attachments')
    if attachments and isinstance(attachments, list) and len(attachments) > 0:
        # Create attachments table with three columns: Number, Name, Link
        attachment_data = [["#", "File Name", "Download Link"]]  # Header row
        
        for idx, attachment in enumerate(attachments, 1):
            if isinstance(attachment, dict):
                name = attachment.get('name', '').strip()
                size = attachment.get('size', 0)
                url = attachment.get('url', '')
                
                # If name is empty, try to extract from URL
                if not name and url:
                    name = url.split('/')[-1] or f'Attachment {idx}'
                elif not name:
                    name = f'Attachment {idx}'
                
                # Format file type
                ext = name.split('.')[-1].upper() if '.' in name else 'File'
                
                # Create clickable link - replace minio:9000 with localhost:9000 for external access
                display_url = url.replace('http://minio:9000', 'http://localhost:9000')
                link_text = f'<a href="{display_url}" color="blue"><u>Download {ext}</u></a>'
                
                attachment_data.append([
                    f"{idx}", 
                    name,
                    link_text
                ])
        
        # Convert attachment data to use Paragraph objects
        formatted_attachment_data = []
        for i, row in enumerate(attachment_data):
            if i == 0:  # Header row
                formatted_attachment_data.append([
                    Paragraph(row[0], label_style),
                    Paragraph(row[1], label_style),
                    Paragraph(row[2], label_style)
                ])
            else:
                formatted_attachment_data.append([
                    Paragraph(row[0], content_style),
                    Paragraph(row[1], content_style),
                    Paragraph(row[2], content_style)
                ])
        
        # Create attachments table with three columns: #, Name, Link
        # Column widths: 10mm for number, 90mm for name, 70mm for link
        attachment_col_widths = [10*mm, 90*mm, 70*mm]
        attachment_table = Table(formatted_attachment_data, colWidths=attachment_col_widths)
        attachment_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Header background
        ]))
        
        # Check if we need a new page
        att_table_width, att_table_height = attachment_table.wrap(width, height)
        if y - att_table_height < 20*mm:
            c.showPage()
            y = height - 20*mm
        
        attachment_table.drawOn(c, 20*mm, y - att_table_height)
    
    c.showPage()
    c.save()
    pdf = buf.getvalue()
    buf.close()
    return pdf
