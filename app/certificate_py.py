from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
import zipfile
from io import StringIO
import io
from reportlab.lib.colors import lightgrey, blue
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

def size_change_px(data):
    return (data*72)/96

def Certificate(date,dateto,supervisor,see,rolePost):
    print(see.gender)
    if see.gender == 'Female':
        heshe = "She"
        himher = "Her"
    elif see.gender == 'Male':
        heshe = "He"
        himher = "Him"
    else:
        heshe = "He/She"
        himher = "Him/Her"

    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    x = size_change_px(725)
    y = size_change_px(419)
    margin = size_change_px(10)
    line_width = size_change_px(5)
    px1 = size_change_px(1)
    px2 = size_change_px(2)
    px3 = size_change_px(3)
    px4 = size_change_px(4)
    px5 = size_change_px(5)
    padding_top = y - (margin + line_width + (px5*6)+px2 + size_change_px(15))

    p = canvas.Canvas(buffer, pagesize=(x, y))
    p.setTitle('certificate')
    p.setFont('Helvetica-Bold', (px5*6)+px2)
    p.drawCentredString(x/2, padding_top, "CERTIFICATE OF INTERNSHIP")
    p.setLineWidth(0.01)
    p.line(x/4, padding_top-(px5*4), x*3/4, padding_top-(px5*4))
    p.setFont('Helvetica', (px5*3)+px3)
    p.drawCentredString(x/2, padding_top-(px5*8)-(px3*3),
                        "THIS CERTIFICATE IS AWAREDED TO")
    pdfmetrics.registerFont(
        TTFont('myfont', 'static/BRUSHSCI.ttf')
    )
    p.setFont('myfont', (px5*10))
    p.drawCentredString(x/2, padding_top-(px5*21)-(px1), str(see.f_name) + " "+ str(see.l_name))
    newpadding = padding_top-(px5*28)-(px3)
    p.setFont('Helvetica-Bold', (px5*3)+px1)
    p.drawCentredString(
        x/2, newpadding, "For outstanding completion of the internship program at")
    p.drawCentredString(x/2, newpadding-(px5*4)-px4,
                        f"________ for the role of {rolePost} under the guidance of {supervisor}")
    p.drawCentredString(x/2, newpadding-(px5*9)-px3,
                        f"from date {date} to {dateto}.")
    p.drawCentredString(x/2, newpadding-(px5*14)-px2,
                        f"{heshe} is found to be hardworking, sincere and diligent. We wish")
    p.drawCentredString(x/2, newpadding-(px5*19)-px1,f"{himher} all the best for future.")
    p.setFont('Helvetica', size_change_px(10))
    p.drawCentredString((x-size_change_px(607)), size_change_px(40), "CEO")
    p.drawCentredString(size_change_px(607), size_change_px(40), "CEO")

    p.setLineWidth(line_width)

    linelist = [(margin, margin-(line_width/2), margin, y-margin+(line_width/2)), (margin, margin, x-margin, margin),
                (margin, y-margin, x-margin, y-margin), (x-margin, margin-(line_width/2), x-margin, y-margin+(line_width/2))]
    p.lines(linelist)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer,see.email_id