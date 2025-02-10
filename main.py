import customtkinter as ctk
import sqlite3
from tkinter import messagebox, ttk
from datetime import date

# This class is to restrict the CTkEntry widget to only accept integers and floats
class NumericEntry(ctk.CTkEntry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(validate="key", validatecommand=(self.register(self._validate), "%P"))

    def _validate(self, P):
        if P == '':
            return True    # Allow empty input

        try:
            float(P)       # Try converting to float. Handles both integers and floats.
            return True
        except ValueError:
            return False   # Reject if not a number


class MainWindow(ctk.CTk):

    ##### My Constants #####

    FONT_BODY = ("Helvetica", 16)
    TRANSPARENT = "transparent"
    U_TAG = "_"         # Uniformity Tag

    ########################

    def __init__(self):    # Constructor
        super().__init__() # Constructor of the Parent Class

        self.title("Expense Tracker")

        self.min_width = 800
        self.min_height = 440
        self.minsize(self.min_width, self.min_height)

        # Default Size
        self.geometry("850x500")

        ##### Heading #####

        self.label = ctk.CTkLabel(self, text="Expense Tracker", font=("Times New Roman", 28))
        self.label.pack(padx=10, pady=10)

        # Columns of the 'Master Frame', and ensures that the table spans the entire width of the window
        self.column_indexes = (0, 1)

        ##### Master Frame config #####

        self.gridFMaster = ctk.CTkFrame(self, fg_color=self.TRANSPARENT)
        self.gridFMaster.pack(pady=8, expand=True, fill=ctk.BOTH)

        self.gridFMaster.columnconfigure(self.column_indexes, uniform=self.U_TAG, weight=1)
        self.gridFMaster.rowconfigure(0, uniform=self.U_TAG, weight=2)
        self.gridFMaster.rowconfigure((1, 2, 3), uniform=self.U_TAG, weight=1)

        ###############################

        ##### Table config #####

        self.table = ttk.Treeview(self.gridFMaster, show="headings",
                                  columns=("date", "description", "income", "expense", "balance"))

        self.table.heading("#1", text="Date")
        self.table.heading("#2", text="Description")
        self.table.heading("#3", text="Income")
        self.table.heading("#4", text="Expense")
        self.table.heading("#5", text="Balance")

        self.table.column("#1", width=120)
        self.table.column("#2", width=180)
        self.table.column("#3", width=140)
        self.table.column("#4", width=140)
        self.table.column("#5", width=140)

        self.table.grid(row=0, column=0, sticky="news", columnspan=len(self.column_indexes))

        self.table.bind("<Delete>", self.delete_selected_rows)

        ########################

        ##### Frame A config #####

        self.gridFrameA = ctk.CTkFrame(self.gridFMaster, fg_color=self.TRANSPARENT)
        self.gridFrameA.grid(row=1, column=0, sticky="news")

        self.gridFrameA.columnconfigure((0, 1), uniform=self.U_TAG, weight=1)
        self.gridFrameA.rowconfigure(0, uniform=self.U_TAG, weight=1)

        ##########################

        ##### Desciption related widgets #####

        self.lblDesc = ctk.CTkLabel(self.gridFrameA, text="Description:", font=self.FONT_BODY)
        self.lblDesc.grid(row=0, column=0, sticky="e")

        self.inputDesc = ctk.CTkEntry(self.gridFrameA, font=self.FONT_BODY)
        self.inputDesc.grid(row=0, column=1, sticky="w", padx=(5, 0))
        self.inputDesc.bind("<KeyRelease>", self.checkInputs)

        ######################################

        ##### Frame B config #####

        self.gridFrameB = ctk.CTkFrame(self.gridFMaster, fg_color=self.TRANSPARENT)
        self.gridFrameB.grid(row=1, column=1, sticky="news")

        self.gridFrameB.columnconfigure(0, uniform=self.U_TAG, weight=1)
        self.gridFrameB.columnconfigure(1, uniform=self.U_TAG, weight=2)
        self.gridFrameB.rowconfigure((0, 1), uniform=self.U_TAG, weight=1)

        ##########################

        ##### Radio Buttons config #####

        self.rb = ctk.IntVar(value=0)

        self.rbIncome = ctk.CTkRadioButton(self.gridFrameB,  text="Income",  font=self.FONT_BODY, value=1, variable=self.rb, command=self.enable_inputAmount)
        self.rbExpense = ctk.CTkRadioButton(self.gridFrameB, text="Expense", font=self.FONT_BODY, value=2, variable=self.rb, command=self.enable_inputAmount)

        self.rbIncome.grid(row=0,  column=0, sticky="sw", pady=(0, 5))
        self.rbExpense.grid(row=1, column=0, sticky="nw", pady=(5, 0))

        ################################

        ##### Amount related widgets #####

        self.packAmountFrame = ctk.CTkFrame(self.gridFrameB, fg_color=self.TRANSPARENT)
        self.packAmountFrame.grid(row=0, column=1, sticky="news", rowspan=2)

        self.lblAmount = ctk.CTkLabel(self.packAmountFrame, text="Amount:", font=self.FONT_BODY)
        self.lblAmount.pack(side=ctk.LEFT, padx=(0, 5))

        self.inputAmount = NumericEntry(self.packAmountFrame, font=self.FONT_BODY, placeholder_text="0.00")
        self.disable_inputAmount()
        self.inputAmount.pack(side=ctk.LEFT)
        self.inputAmount.bind("<KeyRelease>", self.checkInputs)

        ##################################

        ##### 'Add Row' related widgets #####

        self.gridFButton1 = ctk.CTkFrame(self.gridFMaster, fg_color=self.TRANSPARENT)
        self.gridFButton1.grid(row=2, column=0, sticky="news")

        self.button_frame_config(self.gridFButton1)

        self.balances = []           # Values used to populate the "Balance" column in the table
        self.balance_changes = []    # Used to help manage the label relating to 'Total Income' and 'Total Expenses'

        self.btnAddRow = ctk.CTkButton(self.gridFButton1, text="Add Row", font=self.FONT_BODY, state=ctk.DISABLED, command=self.insertRow)
        self.btnAddRow.grid(row=1, column=1, sticky="news")

        ############################################

        ##### 'Delete Row' related widgets #####

        self.gridFButton2 = ctk.CTkFrame(self.gridFMaster, fg_color=self.TRANSPARENT)
        self.gridFButton2.grid(row=3, column=0, sticky="news")

        self.button_frame_config(self.gridFButton2)

        self.btn_delete_last_row = ctk.CTkButton(self.gridFButton2, text="Delete Last Row", font=self.FONT_BODY, state=ctk.DISABLED, command=self.delete_last_row)
        self.btn_delete_last_row.grid(row=1, column=1, sticky="news")

        ########################################

        ##### Totals related widgets #####

        self.gridFrameD = ctk.CTkFrame(self.gridFMaster, fg_color=self.TRANSPARENT)
        self.gridFrameD.grid(row=2, column=1, sticky="news", rowspan=2)

        self.totalIncome = 0
        self.totalExpenses = 0

        self.lbl_totals = ctk.CTkLabel(self.gridFrameD, text="Total Income:\nTotal Expenses:", font=self.FONT_BODY, justify=ctk.LEFT)
        self.lbl_total_vals = ctk.CTkLabel(self.gridFrameD, text="R {0:.2f}\nR {1:.2f}".format(self.totalIncome, self.totalExpenses), font=self.FONT_BODY, justify=ctk.RIGHT)

        self.lbl_totals.pack(side=ctk.LEFT)
        self.lbl_total_vals.pack(side=ctk.LEFT, padx=(100,0))

        ##################################

        self.connection = None

    def __enter__(self):
        self.connection = sqlite3.connect("history.db") # Connect to database "history.db" (implicitly creating it 1st if it doesn't exist)
        self.c = self.connection.cursor()

        self.c.execute("SELECT name FROM sqlite_master WHERE type='table'")
        _db_table = self.c.fetchall()

        if not _db_table: # If the table doesn't exist
            self.c.execute('''
                CREATE TABLE tblHistory (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Date TEXT,
                    Description TEXT,
                    Income REAL,
                    Expense REAL,
                    Balance REAL,
                    Balance_Change REAL
                )
            ''')
        else: # Loading content from the Database
            self.c.execute("SELECT * FROM tblHistory")
            rows = self.c.fetchall()

            for row in rows:
                self.table.insert('',ctk.END, values=(
                    row[1], row[2],
                    f"R {row[3]:.2f}",
                    f"R {row[4]:.2f}",
                    f"R {row[5]:.2f}"
                ))
                self.balances.append(row[5])
                self.balance_changes.append(row[6])

            self.checkRows()

            self.c.execute("SELECT SUM(Income) FROM tblHistory")
            query_output = self.c.fetchone()
            if query_output != None:
                self.totalIncome = query_output[0]
            else:
                self.totalIncome = 0

            self.c.execute("SELECT SUM(Expense) FROM tblHistory")
            query_output = self.c.fetchone()
            if query_output != None:
                self.totalExpenses = query_output[0]
            else:
                self.totalExpenses = 0

            self.refreshLabels()

        return self

    def enable_inputAmount(self):
        self.inputAmount.configure(state=ctk.NORMAL)

    def disable_inputAmount(self):
        self.inputAmount.configure(state=ctk.DISABLED)

    def button_frame_config(self, frame: ctk.CTkFrame):
        frame.columnconfigure(0, uniform=self.U_TAG, weight=3)
        frame.columnconfigure(1, uniform=self.U_TAG, weight=4)
        frame.columnconfigure(2, uniform=self.U_TAG, weight=3)
        frame.rowconfigure(0, uniform=self.U_TAG, weight=2)
        frame.rowconfigure(1, uniform=self.U_TAG, weight=3)
        frame.rowconfigure(2, uniform=self.U_TAG, weight=3)

    def insertRow(self):
        _income = 0
        _expense = 0
        _today = date.today().strftime("%d %b %Y")
        _description = self.inputDesc.get()

        if self.rb.get() == 1:
            _income = float(self.inputAmount.get())
            self.totalIncome += _income
        elif self.rb.get() == 2:
            _expense = float(self.inputAmount.get())
            self.totalExpenses += _expense

        if not self.balances:
            self.balances.append(_income - _expense)
        else:
            self.balances.append(self.balances[-1] + _income - _expense)

        self.balance_changes.append(_income - _expense)

        self.table.insert('', index=ctk.END, values=(
            _today,
            _description,
            f"R {_income:.2f}",
            f"R {_expense:.2f}",
            f"R {self.balances[-1]:.2f}",
        ))

        self.refreshLabels()

        self.inputDesc.delete("0", ctk.END)
        self.inputAmount.delete("0", ctk.END)
        self.disable_inputAmount()
        self.rb.set(-1)
        self.btnAddRow.configure(state=ctk.DISABLED)

        self.checkRows()

        self.c.execute(f'''
            INSERT INTO tblHistory (Date, Description, Income, Expense, Balance, Balance_Change)
            VALUES ('{_today}', '{_description}', '{_income}', '{_expense}', '{self.balances[-1]}', '{self.balance_changes[-1]}')
        ''')

    def delete_selected_rows(self, _):
        _last_selected_item = self.table.selection()[-1]
        _last_item = self.table.get_children()[-1]

        if _last_selected_item == _last_item:
            num_selected_rows = len(self.table.selection())

            for _ in range(num_selected_rows):
                self.delete_last_row(inside_loop=True)

            self.refreshLabels()
            self.checkRows()
        else:
           messagebox.showerror("Invalid Range", "Must select the last row, or last few rows")

    # Used to enable the "Add Row" button if the input fields have content
    def checkInputs(self, _):
        if self.inputDesc.get() and self.inputAmount.get():
            self.btnAddRow.configure(state=ctk.NORMAL)
        else:
            self.btnAddRow.configure(state=ctk.DISABLED)

    # Used to enable the "Delete Last Row" button if rows in the table exist
    def checkRows(self):
        if self.table.get_children():
            self.btn_delete_last_row.configure(state=ctk.NORMAL)
        else:
            self.btn_delete_last_row.configure(state=ctk.DISABLED)

    def refreshLabels(self):
        self.lbl_total_vals.configure(text="R {0:.2f}\nR {1:.2f}".format(self.totalIncome, self.totalExpenses))


    def delete_last_row(self, inside_loop=False):
        self.balances.pop()
        _last_balance_change = self.balance_changes.pop()

        if _last_balance_change < 0:
            self.totalExpenses -= abs(_last_balance_change)
        else:
            self.totalIncome -= abs(_last_balance_change)

        _lastRow = self.table.get_children()[-1]
        self.table.delete(_lastRow)

        if not inside_loop: # Becuase I don't want to unnecessarily call the same method
            self.refreshLabels()
            self.checkRows()

        self.c.execute("DELETE FROM tblHistory WHERE id = (SELECT id FROM tblHistory ORDER BY id DESC LIMIT 1)")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"An exception of type {exc_type} occurred: {exc_val}")
            print(f"Traceback:\n{exc_tb}")
        else:
            if self.connection:
                self.connection.commit()
                self.connection.close()
                self.connection = None # Reset the connection


with MainWindow() as app:
    app.mainloop()
