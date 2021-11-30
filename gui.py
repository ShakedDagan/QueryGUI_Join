import sqlite3
from tkinter import *
from tkinter import ttk


class App:
    def __init__(self):
        print()
        self.root = Tk()
        self.root.geometry("1000x500")
        self.root.title("SQL join query")
        self.root.wm_attributes("-topmost", 1)

        self.leftFrame = Frame(self.root)
        self.leftFrame.pack(side="left")
        self.tables = []
        self.db()
        self.relation = self.dictRelationshipTables()
        self.lb1 = Listbox(self.leftFrame, exportselection=0)
        for i in range(0, len(self.tables)):
            self.lb1.insert(i, self.tables[i])
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
        self.value = [None, None, None]
        self.tree.pack(side='top', padx=30)

        print(self.relation)
        self.root.mainloop()

    def dictRelationshipTables(self):
        relation = dict()
        self.mycursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        for table in self.mycursor.fetchall():
            if table[0] != "sqlite_sequence" and table[0] != "sqlite_stat1":
                relation[table[0]] = dict()
                self.tables.append(table[0])
        for table in self.tables:
            rows = self.mycursor.execute("PRAGMA foreign_key_list({})".format(self.sql_identifier(table)))
            for row in rows.fetchall():
                #print(f'Table: {row[2]}, Field: {row[3]}')
                relation[row[2]][table] = row[3]
                relation[table][row[2]] = row[3]
            #print("\n")
        return relation


    def sql_identifier(self, s):
        return '"' + s.replace('"', '""') + '"'

    def clickListbox1(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        self.value[0] = w.get(index)
        self.value[1] = None
        self.value[2] = None
        print('Listbox 1, You selected item %d: "%s"' % (index, self.value[0]))
        self.data(self.conn, self.mycursor, self.tree, self.value, 1)
        self.updateListbox(2, self.relation[self.value[0]])
        self.updateListbox(3, [])

    def clickListbox2(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        self.value[1] = w.get(index)
        self.value[2] = None
        print('Listbox 2, You selected item %d: "%s"' % (index, self.value[1]))
        self.data(self.conn, self.mycursor, self.tree, self.value, 2)
        self.updateListbox(3, self.relation[self.value[1]])

    def clickListbox3(self, event):
        w = event.widget
        index = int(w.curselection()[0])
        self.value[2] = w.get(index)
        print('Listbox 3, You selected item %d: "%s"' % (index, self.value[2]))
        self.data(self.conn, self.mycursor, self.tree, self.value, 3)

    def updateListbox(self, num, dict_tables):
        lb = [self.lb1, self.lb2, self.lb3]
        if num < 1:
            return
        lb[num-1].delete(0, END)
        for index, key in enumerate(dict_tables):
            if key not in self.value:
                lb[num - 1].insert(index, key)

    def db(self):
        self.conn = sqlite3.connect('chinook.db')
        self.mycursor = self.conn.cursor()


    def data(self, conn, mycursor, tree, tables, numOfTables):
        for x in tree.get_children():
            tree.delete(x)
        select_query = f'SELECT *  FROM {tables[0]}'
        where_query = f' WHERE '
        for i in range(numOfTables-1):
            if i > 0:
                where_query += ' AND '
            select_query += f', {tables[i+1]}'
            where_query += f'{tables[i]}.{self.relation[tables[i]][tables[i+1]]} = {tables[i+1]}.{self.relation[tables[i+1]][tables[i]]}'
        #print(where_query)
        if numOfTables == 1:
            where_query = ''
        query = select_query + where_query
        print(query)
        mycursor.execute(query)
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
