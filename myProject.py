from tkinter import *
from tkinter import ttk
import sqlite3

root = Tk()
root.geometry("500x500")
root.title("Artist, Albums, Tracks")

def db(tree):
    conn = sqlite3.connect('chinook.db')
    mycursor = conn.cursor()
    data(conn, mycursor, tree)

# def on_double_click(self, event):
#     region = self.tree.identify("region", event.x, event.y)
#     if region == "heading":
#         print("1")

def data(conn, mycursor, tree):

    for x in tree.get_children():
        tree.delete(x)
    mycursor.execute("SELECT *  FROM artists, albums, tracks WHERE artists.ArtistId = albums.ArtistId AND albums.AlbumId = tracks.AlbumId")
    for row in mycursor:
         tree.insert('', 'end', values=row[0:10])
    conn.close()

def main():
   root.wm_attributes("-topmost", 1)
   frame = Frame(root)
   frame.pack()
   tree = ttk.Treeview(frame, columns = (1,2,3,4,5,6,7), \
                    height = 20, show = "headings")
   # tree.bind("<Double-1>", on_double_click)

   tree.pack(side = 'top')

   tree.heading(1, text="AlbumId")
   tree.heading(2, text="Title")
   tree.heading(3, text="ArtistId")
   tree.heading(4, text="artists.Name")
   tree.heading(5, text="tracks.Name")
   tree.heading(6, text="UnitPrice")
   tree.heading(7, text="Composer")

   for i in range(1, 7):
       tree.column(i, width=150)

   db(tree)
   root.mainloop()

main()
