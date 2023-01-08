def size_change_px(data):
    return (data*72)/96

# importing modules
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib import colors
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
import zipfile
from io import StringIO
import os
import io
x = size_change_px(595)
y = size_change_px(842)
margin = size_change_px(20)
line_width = size_change_px(2)
px1 = size_change_px(1)
px2 = size_change_px(2)
px3 = size_change_px(3)
px4 = size_change_px(4)
px5 = size_change_px(5)
px7 = size_change_px(7)
buffer = io.BytesIO()
p = canvas.Canvas(buffer, pagesize=(x, y))
p.rect(size_change_px(60), size_change_px(750),
        size_change_px(60), size_change_px(30), stroke=1, fill=1)
p.rect(size_change_px(413), size_change_px(790),
        size_change_px(120), size_change_px(20), stroke=1, fill=1)
top = size_change_px(740)
p.setFontSize(size_change_px(18))
p.setLineWidth(line_width)
p.setStrokeColor(colors.lightgrey)
p.line(size_change_px(60), top-size_change_px(18),
        x-size_change_px(60), top-size_change_px(18))
p.setStrokeColor(colors.blue)
p.line(size_change_px(60), top-size_change_px(18),
        size_change_px(150), top-size_change_px(18))
linelist = [(margin, margin-(line_width/2), margin, y-margin+(line_width/2)), (margin, margin, x-margin, margin),
            (margin, y-margin, x-margin, y-margin), (x-margin, margin-(line_width/2), x-margin, y-margin+(line_width/2))]
p.lines(linelist)
p.drawCentredString(x/2, top, "Internship Offer Letter")

gap = size_change_px(5)
p.setFontSize(size_change_px(14))
p.drawString(size_change_px(60), top-size_change_px(36)-px7, "Company")
p.drawString(size_change_px(60), top-size_change_px(36)-(px7*4), "Date")
p.drawString(size_change_px(60), top-size_change_px(36)-(px7*7), "Name")
p.drawString(size_change_px(60), top-size_change_px(36)-(px7*10), "Collage Name")
p.drawString(size_change_px(60), top-size_change_px(36)-gap-(px7*13), "Sub: Internship")
p.drawString(size_change_px(60), top-size_change_px(36)-(gap*2)-(px7*16), "Dear Name")
mystyle = ParagraphStyle('style',
fontSize = px7*2,
leading= (px7*2)+px5)
p1 = Paragraph('''We are pleased to offer you an educational internship opportunity as [Profile].
You will report directly to [Name] Your immediate supervisor will be [Name].
We trust that your knowledge, skills and experience will be among our
most valuable assets.<br/>
As discussed, and agreed with you, the internshp is paid upto [Amount] INR , and company
will not be liable for any kind of other monetary components/benefits. Your role and salary
structure will be revised if we will hire you in future.<br/>
This offer letter must be signed within 10 days from 19 Nov 2022. Please send asigned
copy of this letter indicating your acceptance to join us or you can reply to mail only before
this date.<br/>
Upon acceptance of our offer, This Offer letter will be treated as Joining letter and Other
joining formalities will be carried out through mail as for remote internship. Also If you will
not perform well during this internship, we can terminate your internship without prior
notice.<br/>
We look forward to welcome you aboard.<br/>
With Best Regards,<br/>
''',mystyle)
p1.wrapOn(p,x-(px5*24),(px7*15))
p1.drawOn(p,size_change_px(60), top-size_change_px(36)-(gap*3)-(px7*63)-px1)
p.drawString(size_change_px(60), top-size_change_px(36)-(gap*4)-(px7*65),"Sincerely")
p.drawString(size_change_px(60), top-size_change_px(36)-(gap*5)-(px7*68),"Name")
p.drawString(size_change_px(60), top-size_change_px(36)-(gap*5)-(px7*71),"Rank,")
p.drawString(size_change_px(60), top-size_change_px(36)-(gap*5)-(px7*74),"Company")
p.setStrokeColor(colors.lightgrey)
bottom = (size_change_px(40))+(px7*9)
p.line(size_change_px(60), bottom,
        x-size_change_px(60), bottom)
p.setStrokeColor(colors.blue)
p.line(size_change_px(60), bottom,
        size_change_px(150), bottom)
bottomgap = size_change_px(158.3)
bottomlinedown = bottom-(px7*6)
bottomtext = bottom-(px7*4)
p.drawCentredString(size_change_px(60)+ (bottomgap/2), bottomtext ,"[email]")
p.drawCentredString(size_change_px(60)+ (bottomgap*3/2), bottomtext ,"[website]")
email = "[address]"
mystyle2 = ParagraphStyle('style2',
alignment=TA_CENTER,
)

if len(email)<=15:
    p2=Paragraph(email, mystyle2)
    p2.wrapOn(p,bottomgap,(px7*15))
    p2.drawOn(p,size_change_px(60)+(bottomgap*2), bottomtext)
elif len(email)<=30:
    p2 = Paragraph(email[:15] + " <br/> " + email[15:], mystyle2)
    p2.wrapOn(p,bottomgap,(px7*15))
    p2.drawOn(p,size_change_px(60)+(bottomgap*2), bottomtext-(px7*3))
else:
    p2=Paragraph("email length is unusual", mystyle2)
    p2.wrapOn(p,bottomgap,(px7*15))
    p2.drawOn(p,size_change_px(60)+(bottomgap*2), bottomtext)


# p.drawCentredString(size_change_px(60)+ (bottomgap*5/2), bottomtext ,"123456789012345")

p.line(size_change_px(60)+bottomgap, bottom-px7-px5,
        size_change_px(60)+bottomgap, bottomlinedown)
p.line(size_change_px(60)+(bottomgap*2), bottom-px7-px5,
        size_change_px(60)+(bottomgap*2), bottomlinedown)



p.showPage()
p.save()
buff = io.BytesIO()
with zipfile.ZipFile("data.zip",'w',compression=zipfile.ZIP_DEFLATED) as file:
    file.writestr('data.pdf',buffer.getvalue())
