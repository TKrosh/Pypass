import smtplib
import json
from email.message import EmailMessage


gmail_cfg = {
 "server" : "smtp.gmail.com",
 "port" : "465",
 "email" : "xxxxxxxxxx@gmail.com",
 "pwd" : "xxxxxxxxxxxxxxxxxxxx"
}

msg = EmailMessage()

msg["to"] = gmail_cfg["email"]
msg["from"] = gmail_cfg["email"]
msg["Subject"] = "Send email with Python"
msg.set_content("this email was sent from Python script !")

with smtplib.SMTP_SSL(host=gmail_cfg["server"], port=gmail_cfg["port"]) as smtp:
    smtp.ehlo()
    smtp.login(gmail_cfg["email"],gmail_cfg["pwd"])
    smtp.send_message(msg)
    smtp.close()
    print("Email sent ! ")

"""
xxxxxxxxxxxxxxxxxxxru
xxxxxxxxxxxxxxxxxxru
xxxxxxxxxxxxxxxxxcom
xxxxxxxxxxxxxxxxxxxx
"""