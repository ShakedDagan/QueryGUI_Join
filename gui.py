import sqlite3
from tkinter import *
from tkinter import ttk


class App:
    """
    A class used to create an App

    ...

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """

    def __init__(self):

        self.root = Tk()
        self.root.geometry("1000x550")
        self.root.title("SQL join query Shaked Dagan")
        self.root.resizable(0, 0)
        # self.root.wm_attributes("-topmost", 1)

        tables = []  # array for holding all table names
        self.conn = None
        self.mycursor = self.db('chinook.db')  # function to connect to the database
        self.relation = dictRelationshipTables(self.mycursor,
                                               tables)  # analyze the database with all the relations (keys,tables)

        self.leftFrame = Frame(self.root)  # divide program into 2 frames left and right
        self.leftFrame.pack(side="left")

        self.rightFrame = Frame(self.root, width=500, height=500)
        self.rightFrame.pack(side="right")

        self.frame_query = Frame(self.rightFrame)  # small frame for query label
        self.frame_query.pack(side='top')

        self.var = StringVar()
        self.label_query = Label(self.frame_query, textvariable=self.var,
                                 wraplength=450, font=("Arial", 11), pady=10, height=4)
        self.var.set("Query")  # Query label with StringVar
        self.label_query.pack()

        self.statistics = StringVar()
        self.statistics.set('Number of Columns: 0\nNumber of Rows: 0')
        self.label_statistics = Label(self.leftFrame,  # statistics label with StringVar
                                      textvariable=self.statistics, pady=20, anchor="w", wraplength=250)
        self.label_statistics.grid(row=2, column=1, sticky='w')

        self.join_columns = StringVar()
        self.join_columns.set('Join Columns:\tNone')  # join columns label with StringVar
        self.join_columns_label = Label(self.leftFrame,
                                        textvariable=self.join_columns, anchor='n', height=6)
        self.join_columns_label.grid(row=3, column=0, columnspan=3, rowspan=1, sticky="nswe")

        self.lb1_frame = Frame(self.leftFrame)
        self.lb1_frame.grid(row=1, column=0, padx=10)  # frame and Listbox for the 1st table pick
        self.lb1 = Listbox(self.lb1_frame, exportselection=0)
        for i in range(0, len(tables)):  # inserting to the first listbox all the table names in the DB
            self.lb1.insert(i, tables[i])
        self.lb1.pack(side='left')

        self.lb2_frame = Frame(self.leftFrame)
        self.lb2_frame.grid(row=1, column=1, padx=10)  # frame and Listbox for the 2nd table pick
        self.lb2 = Listbox(self.lb2_frame, exportselection=0)
        self.lb2.pack(side='left')

        self.lb3_frame = Frame(self.leftFrame)
        self.lb3_frame.grid(row=1, column=2, padx=10)  # frame and Listbox for the 3rd table pick
        self.lb3 = Listbox(self.lb3_frame, exportselection=0)
        self.lb3.pack(side='left')

        vsb_lb1 = ttk.Scrollbar(self.lb1_frame, orient="vertical", command=self.lb1.yview)
        vsb_lb1.pack(side='right', fill='y')  # scrollbar to move around the 1st listbox
        self.lb1.config(yscrollcommand=vsb_lb1.set)

        vsb_lb2 = ttk.Scrollbar(self.lb2_frame, orient="vertical", command=self.lb2.yview)
        vsb_lb2.pack(side='right', fill='y')  # scrollbar to move around the 2nd listbox
        self.lb2.config(yscrollcommand=vsb_lb2.set)

        vsb_lb3 = ttk.Scrollbar(self.lb3_frame, orient="vertical", command=self.lb3.yview)
        vsb_lb3.pack(side='right', fill='y')  # scrollbar to move around the 3rd listbox
        self.lb3.config(yscrollcommand=vsb_lb3.set)

        self.label_table1 = Label(self.leftFrame, text="Table 1", font=("Arial", 11))
        self.label_table1.grid(row=0, column=0)  # label for the 1st Table

        self.label_table2 = Label(self.leftFrame, text="Table 2", font=("Arial", 11))
        self.label_table2.grid(row=0, column=1)  # label for the 2nd Table

        self.label_table3 = Label(self.leftFrame, text="Table 3", font=("Arial", 11))
        self.label_table3.grid(row=0, column=2)  # label for the 3rd Table

        self.tree_frame = Frame(self.rightFrame)
        # pack the frame where the tree will be held to the right frame
        self.tree_frame.pack(padx=30, pady=15, fill='y')
        # creating a new tree
        self.tree = ttk.Treeview(self.tree_frame, columns=(1, 2, 3), height=20, show="headings")

        vsb = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        vsb.pack(side='right', fill='y')  # scrollbar for the tree view vertical
        self.tree.configure(yscrollcommand=vsb.set)

        hsb = ttk.Scrollbar(self.tree_frame, orient="horizontal", command=self.tree.xview)
        hsb.pack(side='bottom', fill='x')  # scrollbar for the tree view horizontal
        self.tree.configure(xscrollcommand=hsb.set)

        self.tree.pack(fill='y')  # pack the tree to the frame

        self.lastClick = '#1'  # representing the last column the user has clicked on (sorting the col in reverse)
        self.tree.bind("<Button-1>", self.on_click)  # event happening on click on the tree view

        self.lb1.bind('<<ListboxSelect>>', self.clickListbox1)  # binding click to the 1st listbox
        self.lb2.bind('<<ListboxSelect>>', self.clickListbox2)  # binding click to the 2nd listbox
        self.lb3.bind('<<ListboxSelect>>', self.clickListbox3)  # binding click to the 3rd listbox

        self.value = [None, None, None]  # hold tables marked in the listboxes

        self.root.mainloop()  # Infinite run the program

    def clickListbox1(self, event):
        """Gets event
        listbox mark table event handler, showing query result from database to the treeview
        and updating the 2nd listbox to show new tables"""
        w = event.widget
        index = int(w.curselection()[0])
        self.value[0] = w.get(index)
        self.value[1] = None
        self.value[2] = None
        self.data(self.mycursor, self.tree, self.value, 1)
        self.updateListbox(2, self.relation[self.value[0]])
        self.updateListbox(3, [])

    def clickListbox2(self, event):
        """Gets event
                listbox mark table event handler, showing query result from database to the treeview
                and updating the 3rd listbox to show new tables"""
        w = event.widget
        index = int(w.curselection()[0])
        self.value[1] = w.get(index)
        self.value[2] = None
        self.data(self.mycursor, self.tree, self.value, 2)
        self.updateListbox(3, self.relation[self.value[1]])

    def clickListbox3(self, event):
        """Gets event
            listbox mark table event handler, showing query result from database to the treeview
            """
        w = event.widget
        index = int(w.curselection()[0])
        self.value[2] = w.get(index)
        self.data(self.mycursor, self.tree, self.value, 3)

    def updateListbox(self, num, dict_tables):
        """Updating new items in listbox according to the ones who got clicked

                        Parameters
                        ----------
                        num : int
                            integer showing what listbox needed to be updated
                        dict_tables: dictionary(string:string)
                            dictionary representing the tables that can join to the current table
                    """
        lb = [self.lb1, self.lb2, self.lb3]
        if num < 1:
            return
        lb[num - 1].delete(0, END)
        for index, key in enumerate(dict_tables):
            if key not in self.value:
                lb[num - 1].insert(index, key)

    def db(self, db):
        """Gets db string location  Returns cursor pointing to the database"""
        self.conn = sqlite3.connect(db)
        return self.conn.cursor()

    def data(self, mycursor, tree, tables, num_of_tables):
        for x in tree.get_children():
            tree.delete(x)
        select_query = f'SELECT *  FROM {tables[0]}'
        where_query = f' WHERE '
        join_column = ''
        for i in range(num_of_tables - 1):
            if i > 0:
                where_query += ' AND '
            join_column += f'Keys:\tTable: {tables[i]}     Column: {self.relation[tables[i]][tables[i + 1]]}' \
                           f'\n\tTable: {tables[i + 1]}     Column: {self.relation[tables[i + 1]][tables[i]]}\n\n'
            select_query += f', {tables[i + 1]}'
            where_query += f'{tables[i]}.{self.relation[tables[i]][tables[i + 1]]} = {tables[i + 1]}.{self.relation[tables[i + 1]][tables[i]]}'
        if num_of_tables == 1:
            where_query = ''
            join_column = 'Join Columns:\tNone'
        self.join_columns.set(join_column)
        query = select_query + where_query

        data = mycursor.execute(query)
        rows = mycursor.fetchall()
        rows_num = len(rows)
        param = [i for i in range(1, len(data.description) + 1)]
        tree.configure(columns=param)
        self.var.set(query)

        for index, column in enumerate(data.description):
            tree.heading(index + 1, text=column[0])
            tree.column(index + 1, width=88, stretch=NO)

        for row in rows:
            tree.insert('', 'end', values=row)

        treeview_sort_column(tree, 0, False)
        self.statistics.set(f'Number of Columns: {len(data.description)}\nNumber of Rows: {rows_num}')

    def on_click(self, event):
        """Mouse click event handler, sorting the column in treeview whenever clicked

                Parameters
                ----------
                event : event
                    event showing info about the mouse click
            """
        region = self.tree.identify("region", event.x, event.y)
        if region == "heading":
            col = self.tree.identify_column(event.x)
            if self.lastClick is None or self.lastClick != col:
                self.tree.heading(col, command=lambda: treeview_sort_column(self.tree, col, False))
                self.lastClick = col


def treeview_sort_column(tv, col, reverse):
    """Sorting given tree by his column + option to reverse it by clicking on the same column

        Parameters
        ----------
        tv : treeview
            treeview showing the database queries
        col : int
            index representing column in the treeview
        reverse: bool
            boolean deciding in what order to sort the column
    """
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


def dictRelationshipTables(mycursor, tables):
    """Gets and returns dict for each table holding its foreign keys

        Parameters
        ----------
        mycursor : cursor
            The mouse cursor handler
        tables : list(str)
            list representing all the tables names in the database

        Returns
        -------
        dictionary
            a dict representing each table as a dict holding its foreign keys
    """
    relation = dict()
    mycursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    for table in mycursor.fetchall():
        if table[0] != "sqlite_sequence" and table[0] != "sqlite_stat1":
            relation[table[0]] = dict()
            tables.append(table[0])
    for table in tables:
        rows = mycursor.execute("PRAGMA foreign_key_list({})".format(sql_identifier(table)))
        for row in rows.fetchall():
            relation[row[2]][table] = row[4]
            relation[table][row[2]] = row[3]
    return relation


def sql_identifier(s):
    """ Gets query string and return real sql command (correcting python string limits) """
    return '"' + s.replace('"', '""') + '"'


app = App()
