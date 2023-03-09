from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
from utils.send_email import apsilank_patvirt_email
from lango_geometrija import geometrija

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main_database import Pacientai, Apsilankymai, Daktarai

engine = create_engine("sqlite:///management_system.db")
Session = sessionmaker(bind=engine)
session = Session()


# Naujo apsilankymo pas daktarą  sukūrimas, įdėjimas į duomenų bazę, patikrinimai, ar nėra tuščių laukų.
def naujas_apsilankymas(email):
    def tvirtinti():
        sub1 = aps_data.get()
        sub4 = laikas.get()
        sub2 = priezastis.get()
        sub3 = doctor.get()
        if sub1 == '':
            return messagebox.showerror('Error', 'Įveskite datą!')
        elif sub4 == '':
            return messagebox.showerror('Error', 'Įveskite laiką!')
        elif sub2 == '':
            return messagebox.showerror('Error', 'Įveskite priežastį!')
        elif sub3 == '':
            return messagebox.showerror('Error', 'Pasirinkite gydytoją!')
        else:
            spl = sub3.split()
            spl2 = int(spl[0])
            daktaras = session.query(Daktarai).get(spl2)
            apsilankymo_obj = Apsilankymai(sub1, sub4, sub2)
            pacientas_obj = session.query(Pacientai).get(email)
            pacientas_obj.apsilankymas_rel.append(apsilankymo_obj)
            daktaras.apsilankymas2_rel.append(apsilankymo_obj)
            session.add(apsilankymo_obj)
            session.commit()
            messagebox.showinfo('Result', f"""Apsilankymas sukurtas!
                                             Lauksime jūsų {sub1} dieną, {sub4}!""")
# Patvirtinimas elektroniniu paštu apie užsiregistravimą pas daktarą.
            apsilank_patvirt_email(email, pacientas_obj.vardas, pacientas_obj.pavarde, sub1, sub4, sub2,
                                   daktaras.pavarde, daktaras.specializacija)
            apsilank.destroy()

# Naujo apsilankymo  lango GUI
    apsilank = Toplevel()
    apsilank.title('Naujas apsilankymas')
    geometrija(apsilank, 420, 380)
    aps_data = StringVar()
    laikas = StringVar()
    priezastis = StringVar()
    doctor = StringVar()

    Label(apsilank, text='Įveskite detales:', font='Helvetica 16 bold', bg='#228498', pady=15, padx=5).grid(row=0, column=1)
    Label(apsilank, text='Įveskite apsilankymo datą:', bg='#228498', pady=5, padx=5).grid(row=2, column=1)
    DateEntry(apsilank, selectmode='day', textvariable=aps_data, date_pattern="yyyy-mm-dd").grid(row=2, column=2, pady=5)
    Label(apsilank, text='Įveskite apsilankymo laiką:', bg='#228498', pady=5, padx=5).grid(row=3, column=1)
    laikai = ['10:00', '10:15', '10:30', '10:45', '11:00', '11:15', '11:30', '11:45', '12:00', '12:15', '12:30',
              '12:45', '13:00', '13:15', '13:30', '13:45', '14:15', '14:30', '14:45', '15:00', '15:15', '15:30',
              '15:45', '16:00', '16:15', '16:30', '16:45', '17:00', '17:15', '17:30', '17:45']
    ttk.Combobox(apsilank, width=12, values=laikai, state='readonly', textvariable=laikas).grid(row=3, column=2, pady=5)
    Label(apsilank, text='Priežastis', bg='#228498', pady=5, padx=5).grid(row=4, column=1, sticky='n')
    Label(apsilank, text='Trumpai nurodykite priežastį', font='Helvetica 8', bg='#228498', padx=5).grid(row=4, column=1, sticky='s')
    Entry(apsilank, width=25, textvariable=priezastis).grid(row=4, column=2, pady=5)
    Label(apsilank, text='Pasirinkite daktarą', bg='#228498', pady=5, padx=5).grid(row=6, column=1)

    daktarai = []
    dr = session.query(Daktarai).all()
    for x in dr:
        listas = f'{x.id} {x.vardas[0]}. {x.pavarde} - {x.specializacija}'
        daktarai.append(listas)
    doctorselect = ttk.Combobox(apsilank, width=23, values=daktarai, state='readonly',
                                textvariable=doctor)
    doctorselect.grid(row=6, column=2, pady=5)
    Button(apsilank, text='Tvirtinti', command=tvirtinti, pady=5).grid(row=8, column=2, pady=15)
