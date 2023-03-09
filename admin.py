from tkinter import messagebox
from tkinter import *
from tkinter import ttk
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main_database import Pacientai, Apsilankymai, Daktarai
import sqlite3
from PIL import ImageTk, Image
from lango_geometrija import geometrija

email = 'kk@kk.lt'
engine = create_engine("sqlite:///management_system.db")
Session = sessionmaker(bind=engine)
session = Session()

conn = sqlite3.connect("management_system.db")
cursor = conn.cursor()

# Administratoriaus puslapis, skirtas valdyti pacientų, apsilankymų ir daktarų informaciją. Pacientus ir apsilankymus
# gali ištrinti, daktarus ištrinti bei juos pridėti. Mato visą turimą informaciją.
def admin_page():
    def atsijungti():
        admin.destroy()
    def refreshas():
        admin.destroy()
        admin_page()
# Apsilankymų lango dalis
    def trinti_apsilankyma():
        trynimas = messagebox.askyesno("", "Ar tikrai norite pašalinti šį apsilankymą?")
        if trynimas > 0:
            try:
                cursor_item = aps_tree.focus()
                item = aps_tree.item(cursor_item)
                final_item = str(item['values'][0])
                del_info = 'DELETE FROM apsilankymai WHERE id=?'
                cursor.execute(del_info, ([final_item]))
                conn.commit()
                selected_item_tree = aps_tree.selection()[0]
                aps_tree.delete(selected_item_tree)
                messagebox.showinfo('Result', "Apsilankymas sėkmingai ištrintas!")
            except IndexError:
                return messagebox.showerror('Error', 'Nepasirinktas joks apsilankymas!')
# Apsilankymų paieška
    def aps_paieska():
        def ieskoti():
            global ieskomas_aps
            ieskomas_aps = search_entry.get().lower()
            search.destroy()
            for record in aps_tree.get_children():
                aps_tree.delete(record)
            rasti_aps_listas = []
            rasti_aps = session.query(Apsilankymai).filter(Apsilankymai.pacientas_id.ilike(ieskomas_aps + '%')).all()
            for x in rasti_aps:
                listas = list((x.id, x.data, x.laikas, x.priezastis, x.daktaras_id, x.pacientas_id))
                rasti_aps_listas.append(listas)
            for i in rasti_aps_listas:
                aps_tree.insert('', 'end', values=i)
# Paieškos lango GUI
        search = Toplevel(admin)
        search.title("Apsilankymų paieška")
        geometrija(search, 400, 200)
        search_frame = LabelFrame(search, text='Paciento el. paštas', bg='#228498')
        search_frame.pack(padx=10, pady=10)
        search_entry = Entry(search_frame, font=('Helvetica 18'))
        search_entry.pack(pady=20, padx=20)

        search_button = Button(search, text='Ieškoti', command=ieskoti)
        search_button.pack(padx=20, pady=20)

        # Pacientu paieška
    def pacientu_paieska():
        def ieskoti():
            global ieskomas_pacientas
            ieskomas_pacientas = search_entry1.get().lower()
            search1.destroy()
            for record in tree.get_children():
                tree.delete(record)
            rasti_aps_listas = []
            rasti_aps = session.query(Pacientai).filter(
                Pacientai.pavarde.ilike(ieskomas_pacientas + '%')).all()
            for x in rasti_aps:
                listas = list((x.vardas, x.pavarde, x.asmens_kodas, x.tel_nr, x.el_pastas, x.lytis, x.gimimo_data))
                rasti_aps_listas.append(listas)
            for i in rasti_aps_listas:
                tree.insert('', 'end', values=i)
        # Paieškos lango GUI
        search1 = Toplevel(admin)
        search1.title("Pacientų paieška")
        search_frame = LabelFrame(search1, text='Paciento pavardė', bg='#228498')
        search_frame.pack(padx=10, pady=10)
        search_entry1 = Entry(search_frame, font=('Helvetica 18'))
        search_entry1.pack(pady=20, padx=20)
        search_button = Button(search1, text='Ieškoti', command=ieskoti)
        search_button.pack(padx=20, pady=20)

    apsilankymai = []
    apsilank = session.query(Apsilankymai).all()
    for x in apsilank:
        listas = list((x.id, x.data, x.laikas, x.priezastis, x.daktaras_id, x.pacientas_id))
        apsilankymai.append(listas)

# PAGRINDINIS USERIO LANGAS  GUI
    admin = Toplevel()
    admin.title('Administratoriaus meniu')
    geometrija(admin, 753, 770)

    img = ImageTk.PhotoImage(Image.open("images/admin_separator.png"))
    label = Label(admin, image=img)
    label.grid(row=0, column=1, pady=10)
    label1 = Label(admin, image=img)
    label1.grid(row=3, column=1, pady=10)
    label2 = Label(admin, image=img)
    label2.grid(row=6, column=1, pady=10)
    label3 = Label(admin, image=img)
    label3.grid(row=9, column=1, pady=20)

    Label(admin, text='Visi apsilankymai', font='Helvetica 16 bold', bg='#228498', pady=20, padx=10).grid(row=0, column=1)
    Label(admin, text='Visi pacientai', font='Helvetica 16 bold', bg='#228498', pady=20, padx=15).grid(row=3, column=1)
    Label(admin, text='Visi gydytojai', font='Helvetica 16 bold', bg='#228498', pady=20, padx=15).grid(row=6, column=1)

# Pasirinkimų meniu
    meniubar = Menu(admin)
    admin.config(menu=meniubar)
    option_meniu = Menu(meniubar)
    meniubar.add_cascade(label='Daugiau pasirinkimų', menu=option_meniu)
    option_meniu.add_command(label='Apsilankymų paieška', command=aps_paieska)
    option_meniu.add_command(label='Pacientų paieška', command=pacientu_paieska)
    option_meniu.add_separator()
    option_meniu.add_command(label='Atsijungti', command=atsijungti)

## Apsilankymų widget (Treeview)
    s = ttk.Style()
    s.theme_use('clam')
    s.configure("Treeview", background="#BDEDF5",
                    foreground="black",
                    fieldbackground="D3D3D3")
    aps_tree = ttk.Treeview(admin, column=("c1", "c2", "c3", "c4", "c5", "c6"), show='headings', height=5)
    aps_tree.grid(row=1, column=1, pady=7)
    aps_tree.column("# 1", anchor=CENTER, width=22)
    aps_tree.heading("# 1", text="ID")
    aps_tree.column("# 2", anchor=CENTER, width=85)
    aps_tree.heading("# 2", text="Data")
    aps_tree.column("# 3", anchor=CENTER, width=65)
    aps_tree.heading("# 3", text="Laikas")
    aps_tree.column("# 4", anchor=CENTER, width=280)
    aps_tree.heading("# 4", text="Nusiskundimas")
    aps_tree.column("# 5", anchor=CENTER, width=130)
    aps_tree.heading("# 5", text="Daktaras")
    aps_tree.column("# 6", anchor=CENTER, width=165)
    aps_tree.heading("# 6", text="Pacientas")
    for i in apsilankymai:
        aps_tree.insert('', 'end', values=i)
    Button(admin, text='Ištrinti apsilankymą', command=trinti_apsilankyma, pady=5).grid(row=2, column=1)
# Pacientų lango dalis
    def trinti_pacienta():
        trynimas = messagebox.askyesno("", "Ar tikrai norite pašalinti šį pacientą?")
        if trynimas > 0:
            try:
                cursor_item = tree.focus()
                item = tree.item(cursor_item)
                final_item = str(item['values'][4])
                del_info = 'DELETE FROM pacientai WHERE el_pastas =?'
                cursor.execute(del_info, ([final_item]))
                conn.commit()
                selected_item_tree = tree.selection()[0]
                tree.delete(selected_item_tree)
                messagebox.showinfo('Result', "Pacientas sėkmingai ištrintas!")
            except IndexError:
                return messagebox.showerror('Error', 'Nepasirinktas joks pacientas!')

    pacientai_list = []
    pacientai = session.query(Pacientai).all()
    for x in pacientai:
        listas = list((x.vardas, x.pavarde, x.asmens_kodas, x.tel_nr, x.el_pastas, x.lytis, x.gimimo_data))
        pacientai_list.append(listas)
    # Pacientų widget (Treeview)
    s = ttk.Style()
    s.theme_use('clam')
    s.configure("Treeview", background="#BDEDF5",
                    foreground="black",
                    fieldbackground="D3D3D3")
    tree = ttk.Treeview(admin, column=("c1", "c2", "c3", "c4", "c5", "c6", "c7"), show='headings', height=5)
    tree.grid(row=4, column=1, pady=7)
    tree.column("# 1", anchor=CENTER, width=100)
    tree.heading("# 1", text="Vardas")
    tree.column("# 2", anchor=CENTER, width=100)
    tree.heading("# 2", text="Pavardė")
    tree.column("# 3", anchor=CENTER, width=100)
    tree.heading("# 3", text="Asmens kodas")
    tree.column("# 4", anchor=CENTER, width=85)
    tree.heading("# 4", text="Tel. nr.")
    tree.column("# 5", anchor=CENTER, width=175)
    tree.heading("# 5", text="El. paštas")
    tree.column("# 6", anchor=CENTER, width=75)
    tree.heading("# 6", text="Lytis")
    tree.column("# 7", anchor=CENTER, width=110)
    tree.heading("# 7", text="Gimimo data")
    for i in pacientai_list:
        tree.insert('', 'end', values=i)
    Button(admin, text='Ištrinti pacientą', command=trinti_pacienta, pady=5, padx=12).grid(row=5, column=1)
# Daktarų lango dalis
    def trinti_daktara():
        try:
            trynimas = messagebox.askyesno("", "Ar tikrai norite pašalinti šį daktarą?")
            if trynimas > 0:
                cursor_item = tree.focus()
                item = tree.item(cursor_item)
                final_item = str(item['values'][4])
                del_info = 'DELETE FROM daktarai WHERE el_pastas =?'
                cursor.execute(del_info, ([final_item]))
                conn.commit()
                selected_item_tree = tree.selection()[0]
                tree.delete(selected_item_tree)
                messagebox.showinfo('Result', "Daktaras sėkmingai ištrintas!")
        except IndexError:
            return messagebox.showerror('Error', 'Nepasirinktas joks daktaras!')

    def prideti_daktara():
        def tvirtinti():
            sub1 = vardas.get().capitalize()
            sub2 = pavarde.get().capitalize()
            sub3 = spec.get().capitalize()
            sub4 = el_pastas.get()
            if sub1 == '':
                return messagebox.showerror('Error', 'Įveskite vardą!')
            elif sub2 == '':
                return messagebox.showerror('Error', 'Įveskite pavardę!')
            elif sub3 == '':
                return messagebox.showerror('Error', 'Įveskite specializaciją!')
            elif sub4 == '':
                return messagebox.showerror('Error', 'Įveskite el. paštą!')
            else:
                daktaras_obj = Daktarai(sub1, sub2, sub3, sub4)
                session.add(daktaras_obj)
                session.commit()
                messagebox.showinfo('Result', "Naujas daktaras sėkmingai įvestas!")
                daktar.destroy()

        # Naujo gydytojo  lango GUI
        daktar = Toplevel()
        daktar.title('Naujas gydytojas')
        geometrija(daktar, 500, 500)
        vardas = StringVar()
        pavarde = StringVar()
        spec = StringVar()
        el_pastas = StringVar()

        Label(daktar, text='Įveskite detales', font='Helvetica 16 bold', bg='#228498', pady=10, padx=5).grid(row=0, column=1)
        Label(daktar, text='Įveskite daktaro vardą:', bg='#228498', pady=5, padx=5).grid(row=2, column=1)
        Entry(daktar, width=25, textvariable=vardas).grid(row=2, column=2, pady=5)
        Label(daktar, text='Įveskite pavardę:', bg='#228498', pady=5, padx=5).grid(row=3, column=1)
        Entry(daktar, width=25, textvariable=pavarde).grid(row=3, column=2, pady=5)
        Label(daktar, text='Įveskite specializaciją:', bg='#228498', pady=5, padx=5).grid(row=4, column=1)
        Entry(daktar, width=25, textvariable=spec).grid(row=4, column=2, pady=5)
        Label(daktar, text='Įveskite el. paštą:', bg='#228498', pady=5, padx=5).grid(row=5, column=1)
        Entry(daktar, width=25, textvariable=el_pastas).grid(row=5, column=2, pady=5)
        Button(daktar, text='Tvirtinti', command=tvirtinti, pady=3).grid(row=8, column=2, pady=10)
        daktar.bind('<Return>', lambda event: tvirtinti())

    daktarai_list = []
    daktarai = session.query(Daktarai).all()
    for x in daktarai:
        listas = list((x.id, x.vardas, x.pavarde, x.specializacija, x.el_pastas))
        daktarai_list.append(listas)
    # Pacientų widget (Treeview)
    s = ttk.Style()
    s.theme_use('clam')
    s.configure("Treeview", background="#BDEDF5",
                    foreground="black",
                    fieldbackground="D3D3D3")
    doc_tree = ttk.Treeview(admin, column=("c1", "c2", "c3", "c4", "c5"), show='headings', height=5)
    doc_tree.grid(row=7, column=1, pady=7)
    doc_tree.column("# 1", anchor=CENTER, width=20)
    doc_tree.heading("# 1", text="ID")
    doc_tree.column("# 2", anchor=CENTER, width=110)
    doc_tree.heading("# 2", text="Vardas")
    doc_tree.column("# 3", anchor=CENTER, width=110)
    doc_tree.heading("# 3", text="Pavardė")
    doc_tree.column("# 4", anchor=CENTER, width=120)
    doc_tree.heading("# 4", text="Specializacija")
    doc_tree.column("# 5", anchor=CENTER, width=175)
    doc_tree.heading("# 5", text="El. paštas")
    for i in daktarai_list:
        doc_tree.insert('', 'end', values=i)
    Button(admin, text='Ištrinti daktarą', command=trinti_daktara, pady=5, padx=13).grid(row=8, column=1)
    Button(admin, text='Pridėti daktarą', command=prideti_daktara, pady=5).grid(row=8, column=1, sticky='w')
    Button(admin, text='Atnaujinti', command=refreshas, padx=16, pady=5).grid(row=8, column=1, sticky='e')


