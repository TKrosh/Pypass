from random import randint
from data import db_session
from data.user import User
import smtplib
from email.mime.text import MIMEText
def send_mail(massage, recipient, theme):
    print('!!!!')
    sender = "passpythonpasspython2023@gmail.com"
    password = "snjicoltzsrxzjrk"

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()

    try:
        server.login(sender, password)
        msg = MIMEText(massage)
        msg["Subject"] = theme
        server.sendmail(sender, recipient, msg.as_string())
        return "OK"
    except Exception as _ex:
        return f'{_ex} PROBLEMS'

def create_password(num, s_let, b_let, sym, long):
    numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    small_letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                     'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                     's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    big_letees = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J',
                  'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                  'U', 'V', 'W', 'X', 'Y', 'Z']
    symbols = ['!', '@', '#', '$', '%', '&']
    materials = []
    result = ''
    if num:
        materials += numbers
    if s_let:
        materials += small_letters
    if b_let:
        materials += big_letees
    if sym:
        materials += symbols
    for i in range(int(long)):
        result += materials[randint(0, len(materials) - 1)]
    return result

def empty_check(some_list):
    #функция нужна, чтобы сраница просмотра не была пустой,
    #в случае если у пользователя нет записей
    if some_list:
        return True
    else:
        return False