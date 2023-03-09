from tkinter import *
from PIL import ImageTk, Image
from tkintermapview import TkinterMapView


def kontaktai_page():
    kontaktai = Toplevel()
    kontaktai['bg'] = '#49A'
    kontaktai.title("Kontaktai")
    width = 600
    height = 600
    screen_width = kontaktai.winfo_screenwidth()
    screen_height = kontaktai.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    kontaktai.geometry('%dx%d+%d+%d' % (width, height, x, y))

    # kontaktai.rowconfigure(0, weight=1)
    # kontaktai.rowconfigure(1, weight=2)
    # kontaktai.rowconfigure(2, weight=2)
    # kontaktai.rowconfigure(3, weight=1)

    Label(kontaktai, text='KONTAKTAI', font='Helvetica 18 bold', fg='#F8FBFB',
          bg='#49A').grid(row=0, column=0, pady=10)

    img = ImageTk.PhotoImage(Image.open("images/kontaktai_img.png"))
    label = Label(kontaktai, image=img)
    label.grid(row=2, column=0, pady=10)
    img1 = ImageTk.PhotoImage(Image.open("images/kontaktai_separator.png"))
    label1 = Label(kontaktai, image=img1)
    label1.grid(row=1, column=0, pady=5)
    # žemėlapio widget'as
    widgetmap = TkinterMapView(kontaktai, width=600, height=300, corner_radius=0)
    widgetmap.grid(row=3, column=0, pady=10)
    widgetmap.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
    widgetmap.set_address("Antakalnio poliklinika", marker=True)

    Label(kontaktai, text='Daugiau informacijos www.antakpol.lt', font='Helvetica 15 bold', fg='#F8FBFB',
          bg='#49A').grid(row=4, column=0, pady=10)

    kontaktai.mainloop()

