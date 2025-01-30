import customtkinter as ctk
from tkinter import ttk

class MainWindow:
    def __init__(self):
        self.root = ctk.CTk()

        self.min_width = 800
        self.min_height = 500
        self.root.minsize(self.min_width, self.min_height)

        ##### My Constants #####
        self.U_TAG = "_" # Uniformity Tag
        self.TRANSPARENT = "transparent"

        ##### Heading #####
        self.label = ctk.CTkLabel(self.root, text="Expense Tracker", font=("Times New Roman", 28))
        self.label.pack(padx=10, pady=10)

        # Columns of the 'Master Frame', and ensures that the table spans the entire width of the window
        self.column_indexes = (0, 1)

        ##### Master Frame config #####

        self.gridFMaster = ctk.CTkFrame(self.root, fg_color=self.TRANSPARENT)
        self.gridFMaster.pack(pady=8, expand=True, fill=ctk.BOTH)

        self.gridFMaster.columnconfigure(self.column_indexes, uniform=self.U_TAG, weight=1)
        self.gridFMaster.rowconfigure(0, uniform=self.U_TAG, weight=2)
        self.gridFMaster.rowconfigure((1, 2, 3, 4), uniform=self.U_TAG, weight=1)

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

        ########################

        # self.table.insert("", index=ctk.END, values=("Abubakr", "Bardien", "abubakrbardien@gmail.com"))

        ##### Frame A config #####

        self.gridFrameA = ctk.CTkFrame(self.gridFMaster, fg_color=self.TRANSPARENT)
        self.gridFrameA.grid(row=1, column=0, sticky="news")

        self.gridFrameA.columnconfigure((0, 1), uniform=self.U_TAG, weight=1)
        self.gridFrameA.rowconfigure(0, uniform=self.U_TAG, weight=1)

        ##########################

        self.font_style_body = ("Helvetica", 16)
        self.labelSpacing = 15 # Helps ensure that "lblDesc" and "lblRowNum" are properly aligned

        ##### Desciption related widgets #####

        self.lblDesc = ctk.CTkLabel(self.gridFrameA, text="Description:", font=self.font_style_body)
        self.lblDesc.grid(row=0, column=0, sticky="e", padx=(0, self.labelSpacing + 19))

        self.inputDesc = ctk.CTkEntry(self.gridFrameA, font=self.font_style_body)
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

        self.radioVar = ctk.IntVar()

        self.rbIncome = ctk.CTkRadioButton(self.gridFrameB,  text="Income",  font=self.font_style_body, value=1, variable=self.radioVar, command=self.enable_inputAmount)
        self.rbExpense = ctk.CTkRadioButton(self.gridFrameB, text="Expense", font=self.font_style_body, value=2, variable=self.radioVar, command=self.enable_inputAmount)

        self.rbIncome.grid(row=0,  column=0, sticky="sw", pady=(0, 5))
        self.rbExpense.grid(row=1, column=0, sticky="nw", pady=(5, 0))

        ################################

        ##### Amount related widgets #####

        self.packAmountFrame = ctk.CTkFrame(self.gridFrameB, fg_color=self.TRANSPARENT)
        self.packAmountFrame.grid(row=0, column=1, sticky="news", rowspan=2)

        self.lblAmount = ctk.CTkLabel(self.packAmountFrame, text="Amount:", font=self.font_style_body)
        self.lblAmount.pack(side=ctk.LEFT, padx=(0, 5))

        self.inputAmount = ctk.CTkEntry(self.packAmountFrame, font=self.font_style_body, placeholder_text="0.0")
        self.inputAmount.configure(state=ctk.DISABLED)
        self.inputAmount.pack(side=ctk.LEFT)

        ##################################

        ##### 'Add Row' related widgets #####

        self.gridFButton1 = ctk.CTkFrame(self.gridFMaster, fg_color=self.TRANSPARENT)
        self.gridFButton1.grid(row=2, column=0, sticky="news")

        self.button_frame_config(self.gridFButton1)

        self.btnAddRow = ctk.CTkButton(self.gridFButton1, text="Add Row", font=self.font_style_body)
        self.btnAddRow.grid(row=1, column=1, sticky="news")

        ############################################

        ##### Frame C config #####

        self.gridFrameC = ctk.CTkFrame(self.gridFMaster, fg_color=self.TRANSPARENT)
        self.gridFrameC.grid(row=3, column=0, sticky="news")

        self.gridFrameC.columnconfigure((0, 1), uniform=self.U_TAG, weight=1)
        self.gridFrameC.rowconfigure(0, uniform=self.U_TAG, weight=1)

        ##########################

        ##### 'Delete Row' related widgets #####

        self.lblRowNum = ctk.CTkLabel(self.gridFrameC, text="Row to Delete:", font=self.font_style_body)
        self.lblRowNum.grid(row=0, column=0, sticky="e", padx=(0, self.labelSpacing))

        self.inputRowNum = ctk.CTkEntry(self.gridFrameC, font=self.font_style_body, placeholder_text="1")
        self.inputRowNum.grid(row=0, column=1, sticky="w", padx=(10, 0))

        self.gridFButton2 = ctk.CTkFrame(self.gridFMaster, fg_color=self.TRANSPARENT)
        self.gridFButton2.grid(row=4, column=0, sticky="news")

        self.button_frame_config(self.gridFButton2)

        self.btnDeleteRow = ctk.CTkButton(self.gridFButton2, text="Delete Row", font=self.font_style_body)
        self.btnDeleteRow.grid(row=1, column=1, sticky="news")

        ########################################

        ##### Totals related widgets #####

        self.gridFrameD = ctk.CTkFrame(self.gridFMaster, fg_color=self.TRANSPARENT)
        self.gridFrameD.grid(row=3, column=1, sticky="news")

        self._var = 95
        self._var2 = 9598

        self.lbl_totals = ctk.CTkLabel(self.gridFrameD, text="Total Income:\nTotal Expenses:", font=self.font_style_body, justify=ctk.LEFT)
        self.lbl_total_vals = ctk.CTkLabel(self.gridFrameD, text="R {0:.2f}\nR {1:.2f}".format(self._var, self._var2), font=self.font_style_body, justify=ctk.RIGHT)

        self.lbl_totals.pack(side=ctk.LEFT)
        self.lbl_total_vals.pack(side=ctk.LEFT, padx=(100,0))

        ##################################

        self.root.mainloop()

    def enable_inputAmount(self):
       self.inputAmount.configure(state=ctk.NORMAL)

    def button_frame_config(self, frame: ctk.CTkFrame):
        frame.columnconfigure(0, uniform=self.U_TAG, weight=3)
        frame.columnconfigure(1, uniform=self.U_TAG, weight=4)
        frame.columnconfigure(2, uniform=self.U_TAG, weight=3)
        frame.rowconfigure(0, uniform=self.U_TAG, weight=2)
        frame.rowconfigure(1, uniform=self.U_TAG, weight=3)
        frame.rowconfigure(2, uniform=self.U_TAG, weight=3)


MainWindow()
