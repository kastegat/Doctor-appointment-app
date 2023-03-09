from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import re
import sqlite3
from utils.send_email import registracija_email
from lango_geometrija import geometrija

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main_database import Pacientai

conn = sqlite3.connect("management_system.db")
cursor = conn.cursor()

engine = create_engine("sqlite:///management_system.db")
Session = sessionmaker(bind=engine)
session = Session()

# Naujo vartotojo sukūrimo funkcija duomenų bazėje su įvesties patikrinimais.
def naujas_useris():
    def nauja_anketa():
        vardas = v.get().capitalize()
        pavarde = p.get().capitalize()
        slaptazodis = s.get()
        asmens_kodas = a.get()
        tel_nr = t.get()
        el_pastas = e.get()
        lytis = l.get().capitalize()
        gim_data = g.get()

        email_obj_list = session.query(Pacientai).filter_by(el_pastas=el_pastas).all()

        if vardas == '':
            return messagebox.showerror('Error', 'Įveskite vardą!')
        elif not vardas.isalpha():
            return messagebox.showerror('Error', 'Vardas negali turėti skaičių!')
        elif pavarde == '':
            return messagebox.showerror('Error', 'Įveskite pavardę')
        elif not pavarde.isalpha():
            return messagebox.showerror('Error', 'Pavardė negali turėti skaičių!')
        elif slaptazodis == '':
            return messagebox.showerror('Error', 'Įveskite slaptažodį!')
        elif asmens_kodas == '':
            return messagebox.showerror('Error', 'Įveskite asmens kodą!')
        elif len(asmens_kodas) != 11:
            return messagebox.showerror('Error', 'Asmens kodas turi būti sudarytas iš 11 skaičių!')
        elif tel_nr == '':
            return messagebox.showerror('Error', 'Įveskite telefono numerį!')
        elif not re.fullmatch('86\d{7}$', tel_nr):
            return messagebox.showerror('Error', 'Telefono numeris netinkamas! Formatas turi būti 86XXXXXXX.')
        elif el_pastas == '':
            return messagebox.showerror('Error', 'Įveskite elektroninį paštą!')
        elif email_obj_list != []:
            return messagebox.showerror('Error', 'Toks el. paštas jau egzistuoja!')
        elif not re.fullmatch("^[0-9a-z._-]+@[0-9a-z._-]+\.[a-z]{2,6}$", el_pastas):
            return messagebox.showerror('Error', 'El. paštas neteisingas!')
        elif lytis == '':
            return messagebox.showerror('Error', 'Įveskite savo lytį!')
        elif gim_data == '':
            return messagebox.showerror('Error', 'Įveskite gimimo datą!')
        else:
            cur = conn.cursor()
            sqlite_insert_with_param = """INSERT INTO pacientai
                      (vardas, pavarde, slaptazodis, asmens_kodas, tel_nr, el_pastas, lytis, gimimo_data) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?);"""
            data_tuple = (vardas, pavarde, slaptazodis, asmens_kodas, tel_nr, el_pastas, lytis, gim_data)
            cur.execute(sqlite_insert_with_param, data_tuple)
            conn.commit()
            messagebox.showinfo('Result', f'Sveikiname prisijungus, {vardas} {pavarde}!')
# Patvirtinimo elektroniniu paštu išsiuntimas
            tema = f'Sveikiname užsiregistravus poliklinikoje, {vardas}!'
            turinys = f'Sveiki, {vardas} {pavarde}! Jūsų registracija pavyko, linkime sėkmės ir lauksime apsilankant!'
            registracija_email(el_pastas, tema, turinys)
            new.destroy()
# Atskiras mygtukas registracijos nutraukimui jos nebaigus
    def nutraukti_reg():
        new.destroy()

# Naujos anketos sukūrimo GUI
    new = Toplevel()
    new.title('Sukurti naują vartotoją')
    geometrija(new, 510, 510)

    v = StringVar()
    p = StringVar()
    s = StringVar()
    a = StringVar()
    t = StringVar()
    e = StringVar()
    l = StringVar()
    g = StringVar()

    Label(new, text='Įveskite savo informaciją:', font='Helvetica 16 bold', pady=15, bg='#228498').grid(row=1, column=2)
    Label(new, text='Įveskite vardą:', bg='#228498', pady=5).grid(row=2, column=1)
    Entry(new, width=25, textvariable=v).grid(row=2, column=2, pady=5)  # vardas
    Label(new, text='Įveskite pavardę:', bg='#228498', pady=5).grid(row=3, column=1)
    Entry(new, width=25, textvariable=p).grid(row=3, column=2, pady=5)  # pavarde
    Label(new, text='Įveskite slaptažodį:', bg='#228498', pady=5).grid(row=4, column=1)
    Entry(new, width=25, textvariable=s, show='*').grid(row=4, column=2, pady=5)  # slaptazodis
    Label(new, text='Įveskite asmens kodą:', bg='#228498', pady=5).grid(row=5, column=1)
    Entry(new, width=25, textvariable=a).grid(row=5, column=2, pady=5)  # asmens kodas
    Label(new, text='Įveskite telefono nr.:', bg='#228498', pady=5).grid(row=6, column=1)
    Entry(new, width=25, textvariable=t).grid(row=6, column=2, pady=5)  # tel nr
    Label(new, text='Įveskite el. paštą:', bg='#228498', pady=5).grid(row=7, column=1)
    Entry(new, width=25, textvariable=e).grid(row=7, column=2, pady=5)  # el pastas
    Label(new, text='Įveskite lytį:', bg='#228498', pady=5).grid(row=8, column=1)
    lytis_values = ['Moteris', 'Vyras', 'Kita']
    ttk.Combobox(new, width=20, values=lytis_values, state='readonly', textvariable=l).grid(row=8, column=2, pady=5)
    Label(new, text='Įveskite gimimo datą:', bg='#228498', pady=5).grid(row=9, column=1)
    DateEntry(new, selectmode='day', textvariable=g, date_pattern="yyyy-mm-dd").grid(row=9, column=2, pady=5)
    Button(new, text='Sukurti vartotoją', command=nauja_anketa, pady=3, padx=11).grid(row=10, column=2, pady=2)
    Button(new, text='Išeiti iš registracijos', command=nutraukti_reg, pady=3).grid(row=12, column=2, pady=2)
