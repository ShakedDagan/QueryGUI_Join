from tkinter import *
from tkinter import ttk
import sqlite3

root = Tk()
root.geometry("500x500")
root.title("Albums")


def db(tree):
    conn = sqlite3.connect('chinook.db')
    mycursor = conn.cursor()
    data(conn, mycursor, tree)


def data(conn, mycursor, tree):

    for x in tree.get_children():
        tree.delete(x)
    mycursor.execute("SELECT *  FROM albums")
    for row in mycursor:
         tree.insert('', 'end', values=row[0:10])
    conn.close()

def main():
   root.wm_attributes("-topmost", 1)
   frame = Frame(root)
   frame.pack()
   tree = ttk.Treeview(frame, columns = (1,2,3), \
                    height = 20, show = "headings")
   tree.pack(side = 'top')

   tree.heading(1, text="AlbumId")
   tree.heading(2, text="Title")
   tree.heading(3, text="ArtistId")

   tree.column(1, width = 100)
   tree.column(2, width = 100)
   tree.column(3, width = 100)

   db(tree)
   root.mainloop()

main()