import sqlite3
from tkinter import *
from tkinter import ttk



class App:
    def __init__(self):
        print()
        self.root = Tk()
        self.root.geometry("1000x550")
        self.root.title("SQL join query")
        # self.root.wm_attributes("-topmost", 1)

        self.leftFrame = Frame(self.root)
        self.leftFrame.pack(side="left")

        self.var = StringVar()
        self.label_query = Label(self.root, textvariable=self.var, wraplength=450, font=("Arial", 11), pady=10)
        self.var.set("Query")
        self.label_query.pack()

        self.tables = []
        self.db()
        self.relation = self.dictRelationshipTables()

        self.statistics = StringVar()
        self.statistics.set('Number of Columns: 0\nNumber of Rows: 0')
        self.label_statistics = Label(self.leftFrame,
                                      textvariable=self.statistics, pady=20, anchor="w")
        self.label_statistics.grid(row=2, column=1, sticky='w')

        self.join_columns = StringVar()
        self.join_columns.set('Join Columns: ')
        self.join_columns_label = Label(self.leftFrame,
                                        textvariable=self.join_columns, anchor="w")
        self.join_columns_label.grid(row=3, column=1, sticky='w', columnspan=2, rowspan=6)

        self.lb1_frame = Frame(self.leftFrame)
        self.lb1_frame.grid(row=1, column=0)
        self.lb1 = Listbox(self.lb1_frame, exportselection=0)
        for i in range(0, len(self.tables)):
            self.lb1.insert(i, self.tables[i])
        self.lb1.pack(side='left')

        self.lb2_frame = Frame(self.leftFrame)
        self.lb2_frame.grid(row=1, column=1)
        self.lb2 = Listbox(self.lb2_frame, exportselection=0)
        self.lb2.pack(side='left')

        self.lb3_frame = Frame(self.leftFrame)
        self.lb3_frame.grid(row=1, column=2)
        self.lb3 = Listbox(self.lb3_frame, exportselection=0)
        self.lb3.pack(side='left')

        vsb_lb1 = ttk.Scrollbar(self.lb1_frame, orient="vertical", command=self.lb1.yview)
        vsb_lb1.pack(side='right', fill='y')
        self.lb1.config(yscrollcommand=vsb_lb1.set)

        vsb_lb2 = ttk.Scrollbar(self.lb2_frame, orient="vertical", command=self.lb2.yview)
        vsb_lb2.pack(side='right', fill='y')
        self.lb2.config(yscrollcommand=vsb_lb2.set)

        vsb_lb3 = ttk.Scrollbar(self.lb3_frame, orient="vertical", command=self.lb3.yview)
        vsb_lb3.pack(side='right', fill='y')
        self.lb3.config(yscrollcommand=vsb_lb3.set)

        self.rightFrame = Frame(self.root, width=500, height=500)
        self.rightFrame.pack(side="right")
        self.tree = ttk.Treeview(self.rightFrame, columns=(1, 2, 3), height=20, show="headings")

        self.label_table1 = Label(self.leftFrame, text="Table 1", font=("Arial", 11))
        self.label_table1.grid(row=0, column=0)

        self.label_table2 = Label(self.leftFrame, text="Table 2", font=("Arial", 11))
        self.label_table2.grid(row=0, column=1)

        self.label_table3 = Label(self.leftFrame, text="Table 3", font=("Arial", 11))
        self.label_table3.grid(row=0, column=2)

        self.lastClick = '#1'
        self.tree.bind("<Button-1>", self.on_click)
        self.lb1.bind('<<ListboxSelect>>', self.clickListbox1)
        self.lb2.bind('<<ListboxSelect>>', self.clickListbox2)
        self.lb3.bind('<<ListboxSelect>>', self.clickListbox3)
        self.value = [None, None, None]

        vsb = ttk.Scrollbar(self.rightFrame, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=vsb.set)

        self.tree.pack(padx=30, fill='y')

        hsb = ttk.Scrollbar(self.rightFrame, orient="horizontal", command=self.tree.xview)
        hsb.pack(side='bottom', fill='x')
        self.tree.configure(xscrollcommand=hsb.set)

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
            print(table)
            for row in rows.fetchall():
                print(row)
                relation[row[2]][table] = row[4]
                relation[table][row[2]] = row[3]
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
        join_column = ''
        for i in range(numOfTables-1):
            if i > 0:
                where_query += ' AND '
            join_column += f'Keys:\tTable: {tables[i]}     Column: {self.relation[tables[i]][tables[i+1]]}' \
                           f'\n\tTable: {tables[i+1]}     Column: {self.relation[tables[i+1]][tables[i]]}\n\n'
            select_query += f', {tables[i+1]}'
            where_query += f'{tables[i]}.{self.relation[tables[i]][tables[i+1]]} = {tables[i+1]}.{self.relation[tables[i+1]][tables[i]]}'
        if numOfTables == 1:
            where_query = ''
            join_column = 'None'
        self.join_columns.set(join_column)
        query = select_query + where_query
        print(query)
        data = mycursor.execute(query)
        rows = mycursor.fetchall()
        rows_num = len(rows)
        param = [i for i in range(1, len(data.description)+1)]
        print(param)
        tree.configure(columns=param)
        self.var.set(query)

        for index, column in enumerate(list(dict.fromkeys(data.description))):
            print(f'index: {index}   column: {column}')
            tree.heading(index+1, text=column[0])
            tree.column(index+1, width=100, stretch=YES)

        for row in rows:
            tree.insert('', 'end', values=row)

        treeview_sort_column(tree, 0, False)
        self.statistics.set(f'Number of Columns: {len(data.description)}\nNumber of Rows: {rows_num}')

    def on_click(self, event):
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

app = App()
