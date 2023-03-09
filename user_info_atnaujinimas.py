from tkinter import *
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3
from lango_geometrija import geometrija
conn = sqlite3.connect("management_system.db")
cursor = conn.cursor()


# Prisijungusio vartotojo informacijos atnaujinimas (ištraukiama informacija iš duomenų bazės ir pakoreguojama,
# ją vėl išsaugant).
def atnaujinimas(email):
    def info_atnaujinimas():
        vardas1 = v.get().capitalize()
        pavarde1 = p.get().capitalize()
        slaptazodis1 = s.get()
        asmens_kodas1 = a.get()
        tel_nr1 = t.get()
        el_pastas1 = e.get()
        lytis1 = l.get().capitalize()
        gim_data1 = g.get()
        if vardas1 == '':
            return messagebox.showerror('Error', 'Įveskite vardą!')
        elif pavarde1 == '':
            return messagebox.showerror('Error', 'Įveskite pavardę')
        elif slaptazodis1 == '':
            return messagebox.showerror('Error', 'Įveskite slaptažodį!')
        elif asmens_kodas1 == '':
            return messagebox.showerror('Error', 'Įveskite asmens kodą!')
        elif tel_nr1 == '':
            return messagebox.showerror('Error', 'Įveskite telefono numerį!')
        elif el_pastas1 == '':
            return messagebox.showerror('Error', 'Įveskite elektroninį paštą!')
        elif lytis1 == '':
            return messagebox.showerror('Error', 'Įveskite savo lytį!')
        elif gim_data1 == '':
            return messagebox.showerror('Error', 'Įveskite gimimo datą!')
        else:
            cursor.execute("""UPDATE pacientai SET
                      vardas = :vardas, 
                      pavarde = :pavarde, 
                      slaptazodis = :slaptazodis,
                      asmens_kodas = :asmens_kodas, 
                      tel_nr = :tel_nr, 
                      el_pastas = :el_pastas, 
                      lytis = :lytis, 
                      gimimo_data = :gim_data

                      WHERE el_pastas = :email""",
                           {'vardas': vardas1,
                            'pavarde': pavarde1,
                            'slaptazodis': slaptazodis1,
                            'asmens_kodas': asmens_kodas1,
                            'tel_nr': tel_nr1,
                            'el_pastas': el_pastas1,
                            'lytis': lytis1,
                            'gim_data': gim_data1,
                            'email': email}
                           )
            conn.commit()
            messagebox.showinfo('Result', f'Informacija atnaujinta!')
            update.destroy()

# Informacijos lango atnaujinimo GUI
    update = Toplevel()
    update.title('Atnaujinti informaciją')
    geometrija(update, 550, 500)

# Prisijungusio  žmogaus  informacijos gavimas
    sql = 'SELECT * FROM pacientai WHERE el_pastas = ?'
    cursor.execute(sql, (email,))
    records = cursor.fetchall()

    v = StringVar()
    p = StringVar()
    s = StringVar()
    a = StringVar()
    t = StringVar()
    e = StringVar()
    l = StringVar()
    g = StringVar()
    Label(update, text='Atnaujinkite informaciją:', font='Helvetica 16 bold', bg='#228498', pady=10, padx=5).grid(row=1, column=1)
    Label(update, text='Įveskite vardą:', bg='#228498', pady=5, padx=5).grid(row=2, column=1)
    vardas = Entry(update, width=25, textvariable=v)
    vardas.grid(row=2, column=2, pady=5)  # vardas
    Label(update, text='Įveskite pavardę:', bg='#228498', pady=5, padx=5).grid(row=3, column=1)
    pavarde = Entry(update, width=25, textvariable=p)
    pavarde.grid(row=3, column=2, pady=5)  # pavarde
    Label(update, text='Įveskite slaptažodį:', bg='#228498', pady=5, padx=5).grid(row=4, column=1)
    slaptazodis = Entry(update, width=25, textvariable=s, show='*')
    slaptazodis.grid(row=4, column=2, pady=5)  # slaptazodis
    Label(update, text='Įveskite asmens kodą:', bg='#228498', pady=5, padx=5).grid(row=5, column=1)
    asm_kodas = Entry(update, width=25, textvariable=a)
    asm_kodas.grid(row=5, column=2, pady=5)  # asmens kodas
    Label(update, text='Įveskite telefono nr.:', bg='#228498', pady=5, padx=5).grid(row=6, column=1)
    tel_nr = Entry(update, width=25, textvariable=t)
    tel_nr.grid(row=6, column=2, pady=5)  # tel nr
    Label(update, text='Įveskite el. paštą:', bg='#228498', pady=5, padx=5).grid(row=7, column=1)
    el_pastas = Entry(update, width=25, textvariable=e)
    el_pastas.grid(row=7, column=2, pady=5)  # el pastas
    Label(update, text='Įveskite lytį:', bg='#228498').grid(row=8, column=1)
    lytis = Entry(update, width=25, textvariable=l)
    lytis.grid(row=8, column=2, pady=5)  # lytis
    Label(update, text='Įveskite gimimo datą:', bg='#228498', pady=5, padx=5).grid(row=9, column=1)
    gim_data = DateEntry(update, width=15, selectmode='day', textvariable=g, date_pattern="yyyy-mm-dd")
    gim_data.grid(row=9, column=2, pady=5)
    gim_data.delete(0, "end")
    Button(update, text='Atnaujinti informaciją', command=info_atnaujinimas, pady=5).grid(row=10, column=2, pady=10)
# Užpildome įvesties langus jau esančiais duomenimis iš duomenų bazės.
    for x in records:
        vardas.insert(0, x[0])
        pavarde.insert(0, x[1])
        slaptazodis.insert(0, x[2])
        asm_kodas.insert(0, x[3])
        tel_nr.insert(0, x[4])
        el_pastas.insert(0, x[5])
        lytis.insert(0, x[6])
        gim_data.insert(0, x[7])

    update.mainloop()

