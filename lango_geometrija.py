def geometrija(x, width, height):
    x['bg'] = '#228498'
    screen_width = x.winfo_screenwidth()
    screen_height = x.winfo_screenheight()
    xx = (screen_width / 2) - (width / 2)
    yy = (screen_height / 2) - (height / 2)
    x.geometry('%dx%d+%d+%d' % (width, height, xx, yy))