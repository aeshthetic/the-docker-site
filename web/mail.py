import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(recipient, subject, body):
    smtp = smtplib.SMTP_SSL(host="smtp.gmail.com", port=465)
    smtp.ehlo()
    smtp.login(os.environ['MAIL_SENDER'], os.environ['MAIL_PASS'])

    msg = MIMEMultipart()
    msg['From'] = os.environ['MAIL_SENDER']
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, "plain"))
    smtp.send_message(msg)
    smtp.quit()
