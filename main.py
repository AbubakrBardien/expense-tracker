import customtkinter as ctk
from tkinter import ttk
from datetime import date

# This class is to restrict the CTkEntry widget to only accept integers and floats
class NumericEntry(ctk.CTkEntry):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(validate="key", validatecommand=(self.register(self._validate), "%P"))

    def _validate(self, P):
        if P == "":
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
    LABEL_SPACING = 15  # Helps ensure that "lblDesc" and "lblRowNum" are properly aligned
    U_TAG = "_"         # Uniformity Tag

    ########################

    def __init__(self):
        super().__init__()

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

        self.table.bind("<Delete>", self.delete_rows_with_keyboard)

        ########################

        ##### Frame A config #####

        self.gridFrameA = ctk.CTkFrame(self.gridFMaster, fg_color=self.TRANSPARENT)
        self.gridFrameA.grid(row=1, column=0, sticky="news")

        self.gridFrameA.columnconfigure((0, 1), uniform=self.U_TAG, weight=1)
        self.gridFrameA.rowconfigure(0, uniform=self.U_TAG, weight=1)

        ##########################

        ##### Desciption related widgets #####

        self.lblDesc = ctk.CTkLabel(self.gridFrameA, text="Description:", font=self.FONT_BODY)
        self.lblDesc.grid(row=0, column=0, sticky="e", padx=(0, self.LABEL_SPACING + 19))

        self.inputDesc = ctk.CTkEntry(self.gridFrameA, font=self.FONT_BODY)
        self.inputDesc.grid(row=0, column=1, sticky="w", padx=(10, 0))

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

        self.inputAmount = NumericEntry(self.packAmountFrame, font=self.FONT_BODY, placeholder_text="0.0")
        self.disable_inputAmount()
        self.inputAmount.pack(side=ctk.LEFT)

        ##################################

        ##### 'Add Row' related widgets #####

        self.gridFButton1 = ctk.CTkFrame(self.gridFMaster, fg_color=self.TRANSPARENT)
        self.gridFButton1.grid(row=2, column=0, sticky="news")

        self.button_frame_config(self.gridFButton1)

        self.running_total = 0
        self.btnAddRow = ctk.CTkButton(self.gridFButton1, text="Add Row", font=self.FONT_BODY, command=self.insertRow)
        self.btnAddRow.grid(row=1, column=1, sticky="news")

        ############################################

        ##### 'Delete Row' related widgets #####

        self.gridFButton2 = ctk.CTkFrame(self.gridFMaster, fg_color=self.TRANSPARENT)
        self.gridFButton2.grid(row=3, column=0, sticky="news")

        self.button_frame_config(self.gridFButton2)

        self.btnDeleteRow = ctk.CTkButton(self.gridFButton2, text="Delete Row", font=self.FONT_BODY, command=self.delete_rows_with_button)
        self.btnDeleteRow.grid(row=1, column=1, sticky="news")

        ########################################

        ##### Totals related widgets #####

        self.gridFrameD = ctk.CTkFrame(self.gridFMaster, fg_color=self.TRANSPARENT)
        self.gridFrameD.grid(row=2, column=1, sticky="news", rowspan=2)

        self._var = 95
        self._var2 = 9598

        self.lbl_totals = ctk.CTkLabel(self.gridFrameD, text="Total Income:\nTotal Expenses:", font=self.FONT_BODY, justify=ctk.LEFT)
        self.lbl_total_vals = ctk.CTkLabel(self.gridFrameD, text="R {0:.2f}\nR {1:.2f}".format(self._var, self._var2), font=self.FONT_BODY, justify=ctk.RIGHT)

        self.lbl_totals.pack(side=ctk.LEFT)
        self.lbl_total_vals.pack(side=ctk.LEFT, padx=(100,0))

        ##################################

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

        if   self.rb.get() == 1:  _income = float(self.inputAmount.get())
        elif self.rb.get() == 2: _expense = float(self.inputAmount.get())

        self.running_total = self.running_total + _income - _expense

        self.table.insert("", index=ctk.END, values=(
            date.today().strftime("%d %b %Y"),
            self.inputDesc.get(),
            "ZAR {:.2f}".format(_income),
            "ZAR {:.2f}".format(_expense),
            "ZAR {:.2f}".format(self.running_total),
        ))

        self.inputDesc.delete("0", ctk.END)
        self.inputAmount.delete("0", ctk.END)
        self.disable_inputAmount()
        self.rb.set(-1)

    def delete_rows_with_keyboard(self, _):
        for row in self.table.selection():
            self.table.delete(row)

    def delete_rows_with_button(self):
        for row in self.table.selection():
            self.table.delete(row)


app = MainWindow()
app.mainloop()
