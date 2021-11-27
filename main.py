from tkinter import *
from tkinter import ttk
import sqlite3

class App:
    def __init__(self):
        self.root = Tk()
        self.root.geometry("500x500")
        self.root.title("Artist, Albums, Tracks")

        self.root.wm_attributes("-topmost", 1)
        self.frame = Frame(self.root)
        self.frame.pack()
        self.tree = ttk.Treeview(self.frame, columns=(1, 2, 3, 4, 5, 6, 7), \
                            height=20, show="headings")
        self.tree.bind("<Double-1>", self.on_double_click)

        self.tree.pack(side='top')

        self.tree.heading(1, text="AlbumId")
        self.tree.heading(2, text="Title")
        self.tree.heading(3, text="ArtistId")
        self.tree.heading(4, text="artists.Name")
        self.tree.heading(5, text="tracks.Name")
        self.tree.heading(6, text="UnitPrice")
        self.tree.heading(7, text="Composer")

        # for i in range(1, 7):
            # self.tree.column(i) #, width=150)

        db(self.tree)
        self.root.mainloop()

    def on_double_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "heading":
            columns = ('AlbumId', 'Title',"ArtistId", 'artists.Name','tracks.Name','UnitPrice','Composer' )
            self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
            for col in columns:
                self.tree.heading(col, text=col, command=lambda: \
                    treeview_sort_column(self.tree, col, True))

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)

    # reverse sort next time
    tv.heading(col, command=lambda: \
           treeview_sort_column(tv, col, not reverse))

def db(tree):
    conn = sqlite3.connect('chinook.db')
    mycursor = conn.cursor()
    data(conn, mycursor, tree)


def data(conn, mycursor, tree):

    for x in tree.get_children():
        tree.delete(x)
    mycursor.execute("SELECT *  FROM artists, albums, tracks WHERE artists.ArtistId = albums.ArtistId AND albums.AlbumId = tracks.AlbumId")
    for row in mycursor:
         tree.insert('', 'end', values=row[0:10])
    conn.close()

# def main():
   # root.wm_attributes("-topmost", 1)
   # frame = Frame(root)
   # frame.pack()
   # tree = ttk.Treeview(frame, columns = (1,2,3,4,5,6,7), \
   #                  height = 20, show = "headings")
   # tree.bind("<Double-1>", on_double_click)
   #
   # tree.pack(side = 'top')
   #
   # tree.heading(1, text="AlbumId")
   # tree.heading(2, text="Title")
   # tree.heading(3, text="ArtistId")
   # tree.heading(4, text="artists.Name")
   # tree.heading(5, text="tracks.Name")
   # tree.heading(6, text="UnitPrice")
   # tree.heading(7, text="Composer")
   #
   # for i in range(1, 7):
   #     tree.column(i, width=150)
   # # tree.column(1, width = 120)
   # # tree.column(2, width = 120)
   # # tree.column(3, width = 120)
   #
   # db(tree)
   # root.mainloop()

# main()
app = App()