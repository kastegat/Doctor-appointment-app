import smtplib
from email.message import EmailMessage
from .prisijungimai import *
from string import Template


def registracija_email(emailas, subject, content):
    email = EmailMessage()
    email["from"] = f"Ligoninės registratūra <{USERNAME}>"
    email["to"] = emailas
    email["subject"] = subject

    email.set_content(content)

    with smtplib.SMTP(host=SMTP_SERVER, port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(USERNAME, PASSWORD)
        smtp.send_message(email)

def apsilank_patvirt_email(emailas, vardas, pavarde, data, laikas, priezastis, daktaras, daktaras_prof):
    with open("utils/html_failas.html", mode="r") as f:
        html = f.read()
    email = EmailMessage()
    email["from"] = f"Ligoninės registratūra <{USERNAME}>"
    email["to"] = emailas
    email["subject"] = 'Apsilankymo poliklinikoje patvirtinimas'

    template = Template(html)
    content = template.substitute({"vardas": vardas,
                                   "pavarde": pavarde,
                                   "data": data,
                                   "laikas": laikas,
                                   "priezastis": priezastis,
                                   "daktaras": daktaras,
                                   "daktaras_prof": daktaras_prof})
    email.set_content(content, "html")

    with smtplib.SMTP(host=SMTP_SERVER, port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login(USERNAME, PASSWORD)
        smtp.send_message(email)