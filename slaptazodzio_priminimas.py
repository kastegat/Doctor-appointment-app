from tkinter import *
from tkinter import messagebox
from utils.send_email import registracija_email
from PIL import ImageTk, Image
from lango_geometrija import geometrija
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main_database import Pacientai

engine = create_engine("sqlite:///management_system.db")
Session = sessionmaker(bind=engine)
session = Session()

# Slaptažodžio primino funkciją, slaptažodis siunčiamas paštu, įvedus registracijos elektroninį paštą.
def slapt_priminimas():
    global img3
    def siusti():
        emailas1 = emailas.get()
        useris = session.query(Pacientai).get(emailas1)
        user_obj_list = session.query(Pacientai).filter_by(el_pastas=emailas1).all()
        if user_obj_list == []:
            return messagebox.showerror('Error', 'Toks el. paštas neegzistuoja!')
        else:
            tema = 'Slaptažodžio priminimas'
            turinys = f'Sveiki, {useris.vardas} {useris.pavarde}. Siunčiame jūsų prisijungimo slaptažodį: {useris.slaptazodis}.'
            registracija_email(emailas1, tema, turinys)
            messagebox.showinfo('Result', f'Slaptažodis išsiųstas į {emailas1}!')
            priminimas.destroy()
# Slaptažodžio priminimo lango GUI
    emailas = StringVar()
    priminimas = Toplevel()
    priminimas.title('Slaptažodžio priminimas')
    geometrija(priminimas, 350, 350)

    img3 = ImageTk.PhotoImage(Image.open("images/slaptazodis_separator.png"))
    label3 = Label(priminimas, image=img3)
    label3.grid(row=1, columnspan=2, pady=10)

    Label(priminimas, text='Priminimas', font='Helvetica 16 bold', bg='#228498', pady=15).grid(row=0, column=0)
    Label(priminimas, text='Įveskite el. paštą,', bg='#228498', padx=5).grid(row=2, column=0)
    Label(priminimas, text='kuriuo registravotės:', bg='#228498', padx=5).grid(row=3, column=0)
    Entry(priminimas, width=20, textvariable=emailas).grid(row=3, column=1, pady=5)
    Button(priminimas, text='Siųsti priminimą', command=siusti, pady=3).grid(row=4, column=1, pady=10)
