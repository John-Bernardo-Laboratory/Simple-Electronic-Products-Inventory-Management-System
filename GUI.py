from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import tkinter as tk

class Items:
    def __init__(self, root):
        self.root = root
        root.iconbitmap("icon.ico")
        self.root.title("Electronic Products Inventory")
        self.root.geometry("1400x650")
        self.root.configure(bg="#f0f0f0")
        self.root.resizable(False, False)
        self.init = False


        style = ttk.Style()
        font_family = "Helvetica"
        style.configure('TButton',
                        borderwidth=0,
                        relief='flat',
                        padding=[-20, 5],
                        font=(font_family, 14))


        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

        self.results_frame = Frame(root, bg="#f0f0f0")
        self.results_frame.pack(side=LEFT, padx=(10, 10), pady=10,anchor="n")

        self.header_frame = Frame(self.results_frame, bg="#f0f0f0")
        self.header_frame.pack(side=TOP, padx=10, pady=10)
        
        self.search_frame = Frame(self.header_frame, bg="#f0f0f0")
        self.search_frame.pack(side=TOP, padx=10, pady=10)

        self.search_label = Label(self.search_frame, text="Search Device:", bg="#f0f0f0", font=(font_family, 14)).pack(side=LEFT)
        self.search_entry = Entry(self.search_frame, width=25, font=(font_family, 16))
        self.search_entry.pack(side=LEFT, padx=(5, 15))

        self.search_button = ttk.Button(self.search_frame, text="Search", command=self.search_devices, style='TButton')
        self.search_button.pack(side=LEFT)

        self.filter_frame = Frame(self.header_frame, bg="#f0f0f0")
        self.filter_frame.pack(side = LEFT, padx=(10, 10), pady=10)

        Label(self.filter_frame, text="Category:", font=(font_family, 14)).pack(side=LEFT)
        self.categoryCombobox = ttk.Combobox(self.filter_frame, width=12,font=(font_family, 12), state="readonly",justify="center")
        self.categoryCombobox.pack(side=LEFT, padx=(10, 10))
        self.categoryCombobox.set("ALL")

        Label(self.filter_frame, text="Tag:", font=(font_family, 14)).pack(side=LEFT)
        self.tagCombobox = ttk.Combobox(self.filter_frame, width=12,font=(font_family, 12), state="readonly", justify="center")
        self.tagCombobox.pack(side=LEFT, padx=(10, 10))
        self.tagCombobox.set("ALL")

        self.filter_label = Label(self.filter_frame, text="Total:", bg="#f0f0f0", font=(font_family, 14)).pack(side=LEFT, padx=(30, 10))
        self.total_products = tk.StringVar(value=0)
        self.total_entry = Entry(self.filter_frame, textvariable=self.total_products, justify='center', width=10, font=(font_family, 16), state='readonly')
        self.total_entry.pack(side=LEFT, padx=(10, 10))

        self.search_entry.focus()
        self.search_entry.bind('<Return>', lambda event: self.search_devices(True))

        self.columns = ("CPN No.", "Product Name", "Product Model","Voltage", "Current","Category", "Quantity", "Condition",  "Tag")
        self.column_config = {
            "CPN No.": ["w", 125],
            "Product Name": ["w", 125],
            "Product Model": ["center", 100],
            "Voltage": ["center", 80],
            "Current": ["center", 80],
            "Category": ["center", 100],
            "Quantity": ["center", 80],
            "Condition": ["center", 100],
            "Tag": ["center", 80]
        }

        self.results_tree = ttk.Treeview(self.results_frame, columns=(self.columns), show='headings', height=30)

        for col in self.columns:
            anchor, width = self.column_config[col]
            self.results_tree.heading(col, text=col, anchor=anchor, command=lambda _col=col: self.sort_by(self.results_tree, _col, False))
            self.results_tree.column(col, width=width, anchor=anchor)

        self.results_tree.pack(side=LEFT, padx=10, pady=10, fill=BOTH, expand=False)

        self.results_tree.bind("<ButtonRelease-1>", self.on_tree_select)

        scrollbar = Scrollbar(self.results_frame, orient=VERTICAL, command=self.results_tree.yview)
        scrollbar.pack(side=LEFT, fill=Y)
        self.results_tree.config(yscrollcommand=scrollbar.set)

        self.param_frame = Frame(root, bg="#f0f0f0")
        self.param_frame.pack(side=RIGHT, padx=(10, 30), pady=10,anchor="n")

        self.nav_frame = Frame(self.param_frame, bg="#f0f0f0")
        self.nav_frame.pack(side=TOP, pady=10, fill=BOTH)

        self.edit_button = ttk.Button(self.nav_frame, text="Edit", command=self.edit_device, style='TButton')
        self.edit_button.pack(side=LEFT, padx=10)

        self.delete_button = ttk.Button(self.nav_frame, text="Delete", command=self.delete_device, style='TButton')
        self.delete_button.pack(side=LEFT, padx=10)

        self.add_button = ttk.Button(self.nav_frame, text="Add", command=self.add_device, style='TButton')
        self.add_button.pack(side=RIGHT, padx=10)

        self.add_button = ttk.Button(self.nav_frame, text="Clear", command=self.clear_entries, style='TButton')
        self.add_button.pack(side=RIGHT, padx=10)

        self.logo_frame = Frame(self.param_frame, bg="#f0f0f0")
        self.logo_frame.pack(side=BOTTOM, padx=10, pady=10, fill=BOTH)

        self.logo = tk.PhotoImage(file="logo.png")
        self.logo_label = tk.Label(self.logo_frame, image=self.logo, bg="#f0f0f0")
        self.logo_label.pack(pady=10)

        self.entry_frame = Frame(self.param_frame, bg="#f0f0f0")
        self.entry_frame.pack(side=BOTTOM, padx=10, pady=10, fill=BOTH)

        self.param_entries = []
        label_width = 18

        spec_title_label = Label(self.entry_frame, text="Parameters", bg="#f0f0f0", font=(font_family, 18, "bold"))
        spec_title_label.grid(row=0, column=0, pady=(0,10), sticky=W)

        for index, label in enumerate(tuple(item for item in self.columns if item != 'Condition')):
            if index == 7:
                Label(self.entry_frame, text="Condition", font=(font_family, 14)).grid(row=8, column=0, pady=10, sticky='w')
                self.conditionCombobox = ttk.Combobox(self.entry_frame, width=20, values=["NEW", "USED", "FOR DISPOSAL"],font=(font_family, 12), state="readonly", justify='center')
                self.conditionCombobox.grid(row=8, column=1, pady=10, sticky=E)
                self.conditionCombobox.set("NEW")
                index +=1
            Label(self.entry_frame, text=label, bg="#f0f0f0", font=(font_family, 14), width=label_width, anchor=W).grid(row= index + 1, column=0, pady=5, sticky=W)
            entry = Entry(self.entry_frame, width=22, font=(font_family, 12), justify='center')
            entry.grid(row= index + 1, column=1, pady=5, sticky=W)
            self.param_entries.append(entry)

        self.search_devices()

    def sort_by(self, tree, col, descending):
        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        data.sort(reverse=descending)

        for index, (val, child) in enumerate(data):
            tree.move(child, '', index)

        tree.heading(col, command=lambda: self.sort_by(tree, col, not descending))

    def create_tables(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS PRODUCTS (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    "CPN No." TEXT,
                    "Product Name" TEXT,
                    "Product Model" TEXT,
                    Voltage TEXT,
                    Current TEXT,
                    Category TEXT,
                    Quantity TEXT,
                    Condition TEXT,
                    Tag TEXT
                )
            ''')

            self.conn.commit()

        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

    def on_tree_select(self, event):
        selected_item = self.results_tree.focus()
        
        if not selected_item:
            return

        item_data = self.results_tree.item(selected_item, 'values')

        self.cursor.execute('SELECT * FROM PRODUCTS WHERE "CPN No." = ? AND "Product Name" = ?', (item_data[0], item_data[1]))
        params = list(self.cursor.fetchone())
        self.conditionCombobox.set(params[len(params)-2])
        params.pop(8)

        for i, param in enumerate(params[1:len(params)]):
            self.param_entries[i].delete(0, END)
            self.param_entries[i].insert(0, param)
    
    def clear_entries(self, event=None):
        if hasattr(self, 'product_name_entry'):
            self.product_name_entry.delete(0, END)
        for entry in self.param_entries:
            entry.delete(0, END)

    def search_devices(self, interupt = False):
        search_term = self.search_entry.get()

        self.cursor.execute('SELECT COUNT("Product Name") FROM PRODUCTS')
        self.total_products.set(self.cursor.fetchone()[0])

        default_values = ["%" + search_term + "%", "%"+ search_term + "%"]
        default_query = f'SELECT * FROM PRODUCTS WHERE ("CPN No." LIKE ? OR "Product Name" LIKE ?) '

        if self.categoryCombobox.get() == "ALL" and self.tagCombobox.get() == "ALL":
            values = []
            query = f'ORDER BY "ID" DESC'
        elif self.tagCombobox.get() == "ALL" and self.categoryCombobox.get() != "ALL":
            values =  [self.categoryCombobox.get()]
            query = f'AND Category = ? ORDER BY "ID" DESC'
        elif self.categoryCombobox.get() == "ALL" and self.tagCombobox.get() != "ALL":
            values =  [self.tagCombobox.get()]
            query = f'AND Tag = ? ORDER BY "ID" DESC'
        else:
            values =  [self.tagCombobox.get() , self.categoryCombobox.get()]
            query = f'AND Tag = ? AND Category = ? ORDER BY "ID" DESC'

        all_rows = []
        self.cursor.execute(default_query + query, (default_values + values))
        rows = self.cursor.fetchall()
        all_rows.extend(rows)

        if rows:   
            self.results_tree.delete(*self.results_tree.get_children())

            self.tag_filter = []
            self.category_filter = []

            for idx, row in enumerate(all_rows):
                row = list(row)[1:]
                self.tag_filter.append(row[8])
                self.category_filter.append(row[5])
                row_tag = 'oddrow' if idx % 2 == 0 else 'evenrow'
                self.results_tree.insert("", "end", values=tuple(row), tags=(row_tag,))
            
            self.tag_filter = list(set(self.tag_filter))
            self.category_filter = list(set(self.category_filter))
            self.tag_filter.insert(0, "ALL")
            self.category_filter.insert(0, "ALL")
            self.tagCombobox.config(values=self.tag_filter)
            self.categoryCombobox.config(values=self.category_filter)

            self.results_tree.tag_configure('evenrow', background='#e7e7e7')
            self.results_tree.tag_configure('oddrow', background='white')
            self.init = True

            children = self.results_tree.get_children()
            if children:
                self.results_tree.selection_set(children[0])
                self.results_tree.focus(children[0])
                self.on_tree_select(None)
        else:
            if self.init:
                self.results_tree.delete(*self.results_tree.get_children())
                messagebox.showerror("Error", "No entries found")

                self.param_entries[0].delete(0, END)
                self.param_entries[0].insert(0, self.search_entry.get())

                for i in range(1,len(self.param_entries)):
                    self.param_entries[i].delete(0, END)
                    self.param_entries[i].insert(0, "")

                self.conditionCombobox.set("NEW")
            else:
                self.init = True

        if interupt:
            self.search_entry.delete(0, END)

    def add_device(self):
        param_values = [entry.get().upper() for entry in self.param_entries if entry.winfo_ismapped()]
        self.categoryCombobox.set("ALL")
        self.tagCombobox.set("ALL")

        if param_values[0] and param_values[1]:
            self.cursor.execute(f'SELECT "CPN No." FROM PRODUCTS WHERE "CPN No." = ? AND "Product Name" = ?', (param_values[0], param_values[1]))
            existing_product = self.cursor.fetchone()

            if existing_product:
                messagebox.showerror("Error", f"Product already exists.")
            else:
                placeholders = ', '.join('?' for _ in range(len(param_values) + 1))
                self.cursor.execute(f'INSERT INTO PRODUCTS {(self.columns)} VALUES ({placeholders})', param_values[0:len(param_values) - 1] + [self.conditionCombobox.get(), param_values[len(param_values) - 1]])
                self.conn.commit()
                self.search_devices()
        else:
            if param_values[1]:
                error = "Please enter a CPN No."
            elif param_values[0]:
                error = "Please enter a Product Name."
            else:
                error = "Please enter a CPN No. and Product Name."

            messagebox.showerror("Error", error)

    def edit_device(self):
        selected_item = self.results_tree.focus()
        item_data = self.results_tree.item(selected_item, 'values')
        
        if not selected_item:
            messagebox.showerror("Error", "Please select a device to edit.")
            return

        if not item_data[0] or not item_data[1]:
            messagebox.showerror("Error", "Could not retrieve device information.")
            return

        confirm = messagebox.askyesno("Confirm Update", f"Are you sure you want to update '{item_data[0]}'?")
        param_values = [entry.get().upper() for entry in self.param_entries if entry.winfo_ismapped()]

        if confirm:
            if param_values[0] and param_values[1]:
                set_clause = ", ".join([f'"{column}" = ?' for column in self.columns])
                self.cursor.execute(f'UPDATE PRODUCTS SET {set_clause} WHERE "CPN No." = ? AND "Product Name" = ?', param_values + [self.conditionCombobox.get(), item_data[0], item_data[1]],)
                self.conn.commit()
                self.search_devices()
            else:
                if param_values[1]:
                    error = "Please enter a CPN No."
                elif param_values[0]:
                    error = "Please enter a Product Name."
                else:
                    error = "Please enter a CPN No. and Product Name."

                messagebox.showerror("Error", error)
    
    def delete_device(self):
        selected_item = self.results_tree.focus()
        item_data = self.results_tree.item(selected_item, 'values')

        if not selected_item:
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this?")
        if confirm: 
            self.cursor.execute(f'DELETE FROM PRODUCTS WHERE "CPN No." = ? AND "Product Name" = ?', (item_data[0],item_data[1]))
            self.conn.commit()
            for entry in self.param_entries:
                entry.delete(0, END)
            self.conditionCombobox.set("NEW")
            self.search_devices()
        
if __name__ == "__main__":
    
    root = Tk()
    app = Items(root)
    root.mainloop()
