from tkinter import *
from tkinter import ttk
import sqlite3


class App:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("1000x500")
        self.root.title("Artist, Albums, Tracks")

        self.root.wm_attributes("-topmost", 1)
        self.frame = Frame(self.root)
        self.frame.pack()
        self.tree = ttk.Treeview(self.frame, columns=(1, 2, 3, 4, 5, 6, 7), \
                                 height=20, show="headings")

        vsb = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)

        vsbX = ttk.Scrollbar(self.frame, orient="horizontal", command=self.tree.xview)
        vsbX.pack(side='bottom', fill='x')
        self.tree.configure(xscrollcommand=vsbX.set)

        #self.tree.bind("<Double-1>", self.on_double_click)
        self.lastClick = None
        self.tree.bind("<Button-1>", self.on_double_click)

        self.tree.pack(side='top')

        self.tree.heading(1, text="AlbumId")
        self.tree.heading(2, text="Title")
        self.tree.heading(3, text="ArtistId")
        self.tree.heading(4, text="artists.Name")
        self.tree.heading(5, text="tracks.Name")
        self.tree.heading(6, text="UnitPrice")
        self.tree.heading(7, text="Composer")

        for i in range(1, 7):
            self.tree.column(i, width=150)

        db(self.tree)
        self.root.mainloop()

    def on_double_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        print(f'click : {region}')
        print(self.tree.identify_column(event.x))
        if region == "heading":
            col = self.tree.identify_column(event.x)
            if self.lastClick is None or self.lastClick != col:
                self.tree.heading(col, command=lambda: treeview_sort_column(self.tree, col, False))
                self.lastClick = col


def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    try:
        l.sort(key=lambda t: int(t[0]), reverse=reverse)

    except ValueError:
        l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))


def db(tree):
    conn = sqlite3.connect('chinook.db')
    mycursor = conn.cursor()
    data(conn, mycursor, tree)


def data(conn, mycursor, tree):
    for x in tree.get_children():
        tree.delete(x)
    mycursor.execute(
        "SELECT *  FROM artists, albums, tracks WHERE artists.ArtistId = albums.ArtistId AND albums.AlbumId = tracks.AlbumId")
    for row in mycursor:
        tree.insert('', 'end', values=row[0:10])
    conn.close()


app = App()
