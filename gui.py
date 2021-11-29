import sqlite3
from tkinter import *
from tkinter import ttk


class App:
    def __init__(self):
        print()
        self.root = Tk()
        self.root.geometry("1000x500")
        self.root.title("Artist, Albums, Tracks")
        self.root.wm_attributes("-topmost", 1)

        self.leftFrame = Frame(self.root)
        self.leftFrame.pack(side="left")
        tables = ["Artists", "Tracks", "Albums", "Genres", "Media_Types", "Playlists", "Playlist_Track", "Invoices", "Invoice_Items", "Customers", "Employees"]
        self.lb1 = Listbox(self.leftFrame, exportselection=0)
        for i in range(0, len(tables)):
            self.lb1.insert(i, tables[i])
        self.lb1.pack(side="left")

        self.lb2 = Listbox(self.leftFrame, exportselection=0)
        self.lb2.pack(side="left")

        self.lb3 = Listbox(self.leftFrame, exportselection=0)
        self.lb3.pack(side="left")

        self.rightFrame = Frame(self.root)
        self.rightFrame.pack(side="right")
        self.tree = ttk.Treeview(self.rightFrame, columns=(1, 2, 3, 4, 5, 6, 7), \
                                 height=20, show="headings")

        self.lb1.bind('<<ListboxSelect>>', self.clickListbox1)
        self.lb2.bind('<<ListboxSelect>>', self.clickListbox2)
        self.lb3.bind('<<ListboxSelect>>', self.clickListbox3)
        self.value1 = None
        self.value2 = None
        self.value3 = None
        self.db()
        self.tree.pack(side='top', padx=30)
        self.relation = self.dictRelationshipTables()
        print(self.relation)
        self.root.mainloop()

    def dictRelationshipTables(self):
        relation = dict()
        self.mycursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = []
        for table in self.mycursor.fetchall():
            if table[0] != "sqlite_sequence" and table[0] != "sqlite_stat1":
                relation[table[0]] = list()
                tables.append(table[0])
        for table in tables:
            rows = self.mycursor.execute("PRAGMA foreign_key_list({})".format(self.sql_identifier(table)))
            for row in rows.fetchall():
                #print(f'Table: {row[2]}, Field: {row[3]}')
                relation[row[2]].append((table, row[3]))
                relation[table].append((row[2], row[3]))
            #print("\n")
        return relation


    def sql_identifier(self, s):
        return '"' + s.replace('"', '""') + '"'

    def clickListbox1(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        self.value1 = w.get(index)
        print('Listbox 1, You selected item %d: "%s"' % (index, self.value1))
        self.data(self.conn, self.mycursor, self.tree, self.value1)
        self.updateListbox(2, [self.value1])
        self.updateListbox(3, [])

    def clickListbox2(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        self.value2 = w.get(index)
        print('Listbox 2, You selected item %d: "%s"' % (index, self.value2))
        self.updateListbox(3, [self.value2])

    def clickListbox3(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        self.value3 = w.get(index)
        print('Listbox 3, You selected item %d: "%s"' % (index, self.value3))

    def updateListbox(self, num, arr):
        lb = [self.lb1, self.lb2, self.lb3]
        if num < 1:
            return
        lb[num-1].delete(0, END)
        for index, value in enumerate(arr):
            lb[num-1].insert(index, value)

    def joinTable(self, ):
        print()

    def db(self):
        self.conn = sqlite3.connect('chinook.db')
        self.mycursor = self.conn.cursor()


    def data(self, conn, mycursor, tree, table):
        for x in tree.get_children():
            tree.delete(x)
        mycursor.execute(
            f'SELECT *  FROM {table}')
        for row in mycursor:
            tree.insert('', 'end', values=row[0:10])


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


app = App()
