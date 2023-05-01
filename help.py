import smtplib
from email.mime.text import MIMEText
from validate_email import validate_email

to_email = "Krashenin2005@mail.ru"
from_email = "passpython@gmail.com"
password = "QWERTY!@324KRO!PROGG"
def send_mail(massage):
    sender = "passpythonpasspython2023@gmail.com"
    password = "snjicoltzsrxzjrk"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    server.login(sender, password)
    msg = MIMEText(massage)
    msg["Subject"] = "подтверждение почты"
    server.sendmail(sender, to_email, msg.as_string())

def main():
    massage = "12321"
    print(send_mail(massage=massage))


if __name__ == "__main__":
    print(validate_email('Krashein2005@mail.ru'))
