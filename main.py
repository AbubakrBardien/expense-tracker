import customtkinter as ctk
from tkinter import ttk

class MainWindow:
    root = ctk.CTk()
    root.geometry("900x600")

    font_style_body = ("Helvetica", 16)

    label = ctk.CTkLabel(root, text="Expense Tracker", font=("Times New Roman", 28))
    label.pack(padx=10, pady=10)

    gridFMaster = ctk.CTkFrame(root, fg_color="transparent")
    gridFMaster.pack(pady=8, fill="both")

    column_indexes = (0, 1)

    gridFMaster.columnconfigure(column_indexes, uniform='_', weight=1)
    gridFMaster.rowconfigure(0, uniform='_', weight=2)
    gridFMaster.rowconfigure((1, 2, 3, 4), uniform='_', weight=1)

    table = ttk.Treeview(gridFMaster, columns=("date", "description", "income", "expense", "balance"), show="headings")

    table.heading("#1", text="Date")
    table.heading("#2", text="Description")
    table.heading("#3", text="Income")
    table.heading("#4", text="Expense")
    table.heading("#5", text="Balance")

    table.column("#1", width=120)
    table.column("#2", width=180)
    table.column("#3", width=140)
    table.column("#4", width=140)
    table.column("#5", width=140)

    table.grid(row=0, column=0, sticky="news", columnspan=len(column_indexes))

    # table.insert("", index=ctk.END, values=("Abubakr", "Bardien", "abubakrbardien@gmail.com"))

    gridFrameA = ctk.CTkFrame(gridFMaster)
    gridFrameA.grid(row=1, column=0, sticky="news")

    gridFrameA.columnconfigure((0, 1), uniform='_', weight=1)
    gridFrameA.rowconfigure(0, uniform='_', weight=1)

    # btn1 = ctk.CTkButton(gridFrame, text="Btn1", font=font_style_body)
    # btn2 = ctk.CTkButton(gridFrame, text="Btn2", font=font_style_body)

    lblDesc = ctk.CTkLabel(gridFrameA, text="Description:", font=font_style_body)
    lblDesc.grid(row=0, column=0, sticky="e", padx=(0,5))

    inputDesc = ctk.CTkEntry(gridFrameA, font=font_style_body)
    inputDesc.grid(row=0, column=1, sticky="w")

    gridFrameB = ctk.CTkFrame(gridFMaster)
    gridFrameB.grid(row=1, column=1, sticky="news")

    gridFrameB.columnconfigure(0, uniform='_', weight=1)
    gridFrameB.columnconfigure(1, uniform='_', weight=2)
    gridFrameB.rowconfigure((0, 1), uniform='_', weight=1)


    # gridFrameB.columnconfigure((0, 1), uniform='_', weight=1)
    # gridFrameB.rowconfigure(0, uniform='_', weight=1)

    radioVar = ctk.IntVar()

    rbIncome = ctk.CTkRadioButton(gridFrameB, text="Income", font=font_style_body, value=1, variable=radioVar)
    rbExpense = ctk.CTkRadioButton(gridFrameB, text="Expense", font=font_style_body, value=2, variable=radioVar)

    # rbIncome.grid(row=0, column=0, sticky="sw", padx=(25, 0), pady=(0, 5))
    # rbExpense.grid(row=1, column=0, sticky="nw", padx=(25, 0), pady=(5, 0))

    rbIncome.grid(row=0, column=0, sticky="s", pady=(0, 5))
    rbExpense.grid(row=1, column=0, sticky="n", pady=(5, 0))

    packAmountFrame = ctk.CTkFrame(gridFrameB)
    packAmountFrame.grid(row=0, column=1, sticky="news", rowspan=2)

    lblAmount = ctk.CTkLabel(packAmountFrame, text="Amount:", font=font_style_body)
    lblAmount.pack(side=ctk.LEFT, padx=(0, 5))
    # lblAmount.grid(row=0, column=1, sticky="w", rowspan=2)

    inputAmount = ctk.CTkEntry(packAmountFrame, font=font_style_body)
    inputAmount.configure(state="disabled")
    inputAmount.pack(side=ctk.LEFT)

    def get_rbtn_val(self):
        print(self.radioVar)

    # lbl1.grid(row=1, column=0, sticky="new", padx=(10, 30), pady=10)
    # lbl1.grid(row=1, column=0, sticky="news", padx=10, pady=10)
    # lbl1.grid(row=1, column=0, padx=10, pady=10)
    # input1.grid(row=1, column=1, sticky="news", padx=10, pady=10)
    # btn1.grid(row=0, column=0, sticky="new", padx=(10, 30), pady=10)
    # btn2.grid(row=1, column=0, sticky="new", padx=(10, 30))

    root.mainloop()

MainWindow()
