import smtplib
from email.mime.text import MIMEText

def sendmail(a):
    sender = 'postman@eknowtek.com'
    recipient = 'chan@eknowtek.com'
    cc = 'chan@eknowtek.com'

    title = 'RMA출고가 등록되었습니다.'
    contents = f"""
작성자: {a.creator}
작성일: {a.created_date}
RMA번호: {a.rma_num}
시리얼번호: {a.serial}
제조사: {a.vendor}
부품명: {a.part}
상태: {a.status}
"""

    msg = MIMEText(contents) # 1

    msg['Subject'] = title # 2
    msg['From'] = sender # 2
    msg['To'] = recipient # 2
    msg['Cc'] = cc # 2

    smtp_server = smtplib.SMTP('mail.eknowtek.com') # 3
    smtp_server.sendmail(from_addr=sender, to_addrs=recipient, msg=msg.as_string()) # 4
    smtp_server.quit() # 5