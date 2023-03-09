import tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import END, Text
from tkmacosx import Button
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main_database import Pacientai
from PIL import ImageTk, Image
import requests
# Puslapių importai
from kontaktai import kontaktai_page
from admin import admin_page
from naujo_apsilankymo_sukurimas import naujas_apsilankymas
from slaptazodzio_priminimas import slapt_priminimas
from naujas_useris import naujas_useris
from user_info_atnaujinimas import atnaujinimas
from lango_geometrija import geometrija

conn = sqlite3.connect("management_system.db")
cursor = conn.cursor()

engine = create_engine("sqlite:///management_system.db")
Session = sessionmaker(bind=engine)
session = Session()

# Pagrindinis vartotojo puslapis, kuriame vartotojas gali matyti savo informaciją, savo būtus ir būsimus apsilankymus
# ir jų informaciją, užregistruoti naują apsilankymą, trinti apsilankymą, atnaujinti savo informaciją, atsijungti.
def vartotojas_pagr():
# Vartotojo  puslapio atnaujinimas
    def refreshas():
        anketa.destroy()
        vartotojas_pagr()
# Apsilankymo trynimas
    def trinti_apsilankyma():
        trinti = tkinter.messagebox.askyesno("", "Ar tikrai norite pašalinti šį apsilankymą?") #papildoma yes or no lentele
        try:
            if trinti > 0:
                cursor_item = tree.focus()
                item = tree.item(cursor_item)
                final_item = str(item['values'][0])
                del_info = 'DELETE FROM apsilankymai WHERE id=?'
                cursor.execute(del_info, ([final_item]))
                conn.commit()
                selected_item_tree = tree.selection()[0]
                tree.delete(selected_item_tree)
                messagebox.showinfo('Result', "Apsilankymas sėkmingai ištrintas!")
        except IndexError:
            return messagebox.showerror('Error', 'Nepasirinktas joks apsilankymas!')
# Atsijungimas iš vartotojo anketos
    def atsijungti():
        anketa.destroy()
# API panaudojimas
    def citata():
        r = requests.get('https://api.quotable.io/random')
        data = r.json()
        citatos = data['content']
        text_box.delete('1.0', END)
        text_box.insert(END, citatos)

# Pagrindinio vartotojo puslapio informacijos surinkimas (informacija apie patį vartotoją iš duomenų bazės).
    sql_skaicius = 'SELECT * FROM apsilankymai where pacientas_id=?'
    cursor.execute(sql_skaicius, (email,))
    c = cursor.fetchall()
    co = str(len(c)) # apsilankymu skaicius
    #########
    sql_vardas = 'SELECT vardas FROM pacientai where el_pastas=?'
    cursor.execute(sql_vardas, (email,))
    row = cursor.fetchall()
    vardas = row[0][0]
    ########
    sql_pavarde = 'SELECT pavarde FROM pacientai where el_pastas=?'
    cursor.execute(sql_pavarde, (email,))
    row1 = cursor.fetchall()
    pavarde = row1[0][0]
    ########
    sql_kodas = 'SELECT asmens_kodas FROM pacientai where el_pastas=?'
    cursor.execute(sql_kodas, (email,))
    row2 = cursor.fetchall()
    kodas = str(row2[0][0])
    ########
    sql_tel = 'SELECT tel_nr FROM pacientai where el_pastas=?'
    cursor.execute(sql_tel, (email,))
    row3 = cursor.fetchall()
    tel = str(row3[0][0])
    ########
    sql_lytis = 'SELECT lytis FROM pacientai where el_pastas=?'
    cursor.execute(sql_lytis, (email,))
    row4 = cursor.fetchall()
    lytis = row4[0][0]
    ########
    sql_gim = 'SELECT gimimo_data FROM pacientai where el_pastas=?'
    cursor.execute(sql_gim, (email,))
    row5 = cursor.fetchall()
    gimimo = str(row5[0][0])
# Ištraukiame informaciją, skirta Treeview widget'ui
    apsilankymai = []
    el_pastas = email  # Paimame email, kuriuo prisijungė vartotojas
    asmuo = session.query(Pacientai).get(el_pastas)
    for x in asmuo.apsilankymas_rel:
        listas = list((x.id, x.data, x.laikas, x.priezastis, x.daktar_rel.pavarde, x.daktaras_id))
        apsilankymai.append(listas)

# Pagrindinio vartotojo lango GUI
    anketa = Toplevel()
    anketa.title('Pagrindinė informacija')
    geometrija(anketa, 716, 620)

    img = ImageTk.PhotoImage(Image.open("images/user_main_separator.png"))
    label = Label(anketa, image=img)
    label.grid(row=10, column=1, pady=10)
    label1 = Label(anketa, image=img)
    label1.grid(row=13, column=1, pady=20)

    text_box = Text(anketa, height=3, width=70, bg="#E9E1C8", fg="black")
    text_box.grid(row=14, column=1, pady=2)
    Button(anketa, text="Pamatykite dienos citatą!", command=citata, pady=1).grid(row=15, column=1)
    Button(anketa, text='Naujas apsilankymas', command=lambda: naujas_apsilankymas(email), pady=2, padx=21).grid(row=2, column=1, sticky='e')
    Button(anketa, text='Ištrinti apsilankymą', command=trinti_apsilankyma, pady=2, padx=26).grid(row=3, column=1, sticky='e')
    Button(anketa, text='Keisti asmeninę informaciją', command=lambda: atnaujinimas(email), pady=2).grid(row=4, column=1, sticky='e')
    Button(anketa, text='Atnaujinti', command=refreshas, pady=2, padx=55).grid(row=5, column=1, sticky='e')
    Button(anketa, text='Atsijungti', command=atsijungti, pady=2, padx=55).grid(row=6, column=1, sticky='e')
    Label(anketa, text='Jūsų informacija', font='Helvetica 16 bold underline', bg='#228498', pady=15, padx=10).grid(row=1, column=1, sticky='w')
    Label(anketa, text='Vardas: ' + vardas, bg='#228498', pady=5, padx=10).grid(row=2, column=1, sticky='w')
    Label(anketa, text='Pavardė: ' + pavarde, bg='#228498', pady=5, padx=10).grid(row=3, column=1, sticky='w')
    Label(anketa, text='Asmens kodas: ' + kodas, bg='#228498', pady=5, padx=10).grid(row=4, column=1, sticky='w')
    Label(anketa, text='Tel. numeris: ' + tel, bg='#228498', pady=5, padx=10).grid(row=5, column=1, sticky='w')
    Label(anketa, text='Lytis: ' + lytis, bg='#228498', pady=5, padx=10).grid(row=6, column=1, sticky='w')
    Label(anketa, text='Gimimo data: ' + gimimo, bg='#228498', pady=5, padx=10).grid(row=7, column=1, sticky='w')
    Label(anketa, text='Apsilankymų skaičius:' + co, bg='#228498', pady=5, padx=10).grid(row=8, column=1, sticky='w')
    Label(anketa, text='Jūsų apsilankymų istorija', font='Helvetica 18 bold underline', bg='#228498', pady=20, padx=10).grid(row=10, column=1)
# Apsilankymų widget (Treeview)
    s = ttk.Style()
    s.theme_use('clam')
    s.configure("Treeview", background="#BDEDF5",
                    foreground="black",
                    fieldbackground="D3D3D3")
    tree = ttk.Treeview(anketa, column=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings', height=5)
    tree.grid(row=12, column=1, pady=5)
    tree.column("# 1", anchor=CENTER, width=15)
    tree.heading("# 1", text="id")
    tree.column("# 2", anchor=CENTER, width=85)
    tree.heading("# 2", text="Data")
    tree.column("# 3", anchor=CENTER, width=65)
    tree.heading("# 3", text="Laikas")
    tree.column("# 4", anchor=CENTER, width=320)
    tree.heading("# 4", text="Nusiskundimas")
    tree.column("# 5", anchor=CENTER, width=110)
    tree.heading("# 5", text="Daktaras")
    tree.column("# 6", anchor=CENTER, width=120)
    tree.heading("# 6", text="El. paštas")
    for i in apsilankymai:
        tree.insert('', 'end', values=i)


# Vartotojo prisijungimas, elektroninio pašto ir slaptažodžio patikrinimas duomenų bazėje.
# Jei viskas tinka, iššoka pagrindinis  vartotojo informacijos langas. Taip pat galima užregistruoti naują vartotoją
# arba pasirinkti slaptažodžio priminimą.
# Iš čia tai pat patenkama į admin meniu (prisijungimas - admin, slaptažodis - admin)
def prisijungimas():
    global img3
    def userio_login():
        global email
        email = em.get().lower()
        password = pasw.get()
        if email == "admin" and password == 'admin':  # admino prisijungimas (galima keisti duomenis ranka)
            prisijungimas.destroy()
            admin_page()
        else:
            user_obj_list = session.query(Pacientai).filter_by(el_pastas=email).all()
            if user_obj_list == []:
                return messagebox.showerror('Error', 'Toks el. paštas neegzistuoja!')
            else:
                user_obj = user_obj_list[0]
            if user_obj.slaptazodis != password:
                return messagebox.showerror('Error', 'Slaptažodis neteisingas!')
            else:
                vartotojas_pagr()
                prisijungimas.destroy()

# Prisijungimo lango GUI
    em = StringVar()
    pasw = StringVar()
    prisijungimas = Toplevel()
    prisijungimas.title("Prisijungimas")
    geometrija(prisijungimas, 504, 504)

    img3 = ImageTk.PhotoImage(Image.open("images/ap_logo1.png"))
    label3 = Label(prisijungimas, image=img3, bd=0)
    label3.grid(row=0, column=1, pady=10)

    Label(prisijungimas, text='Prisijunkite:', font='Arial 18 bold underline', bg='#228498', pady=20).grid(row=1, column=0)
    Label(prisijungimas, text='Įveskite el. paštą:', bg='#228498', font='Arial 14', pady=3, padx=30).grid(row=2, column=0)
    Entry(prisijungimas, width=25, textvariable=em).grid(row=2, column=1,  pady=5)  # email
    Label(prisijungimas, text='Įveskite slaptažodį:', bg='#228498', font='Arial 14', pady=3, padx=30).grid(row=3, column=0)
    Entry(prisijungimas, width=25, textvariable=pasw, show='*').grid(row=3, column=1, pady=5)  # password
    Button(prisijungimas, text='Tęsti', command=userio_login, pady=5).grid(row=4, column=1, pady=4)
    Button(prisijungimas, text='Sukurti naują vartotoją', command=naujas_useris, pady=4).grid(row=5, column=1, pady=5)
    Button(prisijungimas, text='Priminti slaptažodį', command=slapt_priminimas, pady=4).grid(row=6, column=1, pady=5)
# Enter mygtuko paspaudimas
    prisijungimas.bind('<Return>', lambda event: userio_login())

# Pirmojo programos lango GUI
langas = Tk()
langas.title('Ligoninės duomenų bazė')
geometrija(langas, 504, 504)

img1 = ImageTk.PhotoImage(Image.open("images/main_page.png"))
label = Label(langas, image=img1)
label.grid(row=0, column=0)

but_border = LabelFrame(langas, bd=6, bg="white")
but_border.grid(row=0, column=0, sticky='e')
kontakt_border = LabelFrame(langas, bd=6, bg="white")
kontakt_border.grid(row=0, column=0, sticky='se')
Label(langas, text='Sveiki atvykę į Antakalnio polikliniką!', font='Helvetica 14 bold', bg='#228498', padx=4, pady=19).grid(row=0, column=0, sticky='nw')
Button(but_border, bg='#228498', fg='white', text='Prisijungti', command=prisijungimas, bd=1, pady=15, padx=10).grid(row=0, column=0, sticky='e')
Button(kontakt_border, text='Kontaktai', command=kontaktai_page, bg='#228498', fg='white', pady=3, padx=12).grid(row=0, column=0, sticky='se')

langas.mainloop()


