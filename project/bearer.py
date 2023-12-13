from fastapi_sqlalchemy import db
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime
from dotenv import load_dotenv
from .models import Login_code


load_dotenv('.env')


def pdf_maker(items):
    check_login_code=db.session.query(Login_code).first()    
    c=canvas.Canvas("static/Exam_results.pdf")
    c.setFont("Helvetica", 22)
    c.setFillColorRGB(0, 0, 255)
    c.drawString(160,800, "Mugallymlaryn synag netijesi")
    c.drawImage("D:\OnlineTest\images\logo.png", 0.3 * cm, 27 * cm, width=2.5 * cm, height=2.5 * cm)
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0, 0, 255)    
    c.drawString(100,760, "T/b")
    c.drawString(140,760, "Ady")
    c.drawString(290,760, "Familiýasy")
    c.drawString(440,760, "Baly")
    c.setFillColorRGB(0, 0, 0)    
    c.drawString(100,755,"_____________________________________________________________" )
    b1=740
    counter_for_new_page=0
    counter=1
    page_counter=1
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0, 0, 0)
    for i in items:
        if counter_for_new_page==1:
            c.drawString(290,10,f"{page_counter}" )
        counter_for_new_page+=1
        if counter_for_new_page==31:
            counter_for_new_page=1
            page_counter+=1
            c.showPage()
            b1 = 770
        c.drawString(100,b1, f'{counter}')
        c.drawString(140,b1, f"{i.name}")
        c.drawString(290,b1, f"{i.surname}")
        c.drawString(440,b1, f"{i.score}")
        c.drawString(100,b1-5,"_____________________________________________________________" )
        b1=b1-23
        counter+=1
    c.setFont("Helvetica", 12)
    c.setFillColorRGB(0, 0, 0)
    c.drawString(40,70, "Synag wagty")
    gelmesin1=check_login_code.expired_time.hour
    gelsin1=check_login_code.expired_time.minute
    if check_login_code.expired_time.hour<10:
        gelmesin1=f'0{check_login_code.expired_time.hour}'
    if check_login_code.expired_time.minute<10:
        gelmesin1=f'0{check_login_code.expired_time.minute}'
    c.drawString(50,50, f"{gelmesin1}:{gelsin1}")
    c.drawString(250,70, "Sözler toplumy")
    c.drawString(274,50, f"{check_login_code.word_box}")
    c.drawString(460,70, "PDF ýüklenen wagty")
    wagt=datetime.now()
    gelmesin=wagt.hour
    gelsin=wagt.minute
    if wagt.hour<10:
        gelmesin=f'0{wagt.hour}'
    if wagt.minute<10:
        gelsin=f'0{wagt.minute}'
    c.drawString(465,50, f"{wagt.day}.{wagt.month}.{wagt.year} / {gelmesin}:{gelsin}")
    c.save()
    return c._filename