import customtkinter as ctk
from tkinter import ttk

class MainWindow:
    root = ctk.CTk()
    root.geometry("1000x600")

    font_style_body = ("Helvetica", 16)

    label = ctk.CTkLabel(root, text="Expense Tracker", font=("Times New Roman", 28))
    label.pack(padx=10, pady=10)

    frame = ctk.CTkFrame(root, fg_color="transparent")
    frame.pack(pady=10, fill="both")

    frame1 = ctk.CTkFrame(frame, height=400, width=160, fg_color="transparent")
    frame1.pack_propagate(False)
    frame2 = ctk.CTkFrame(frame, fg_color="transparent")

    frame1.pack(side="left")
    frame2.pack(side="right", anchor="n")

    btn1 = ctk.CTkButton(frame1, text="Btn1", font=font_style_body)
    btn1.pack(pady=10)

    btn2 = ctk.CTkButton(frame1, text="Btn2", font=font_style_body)
    btn2.pack(pady=10)

    table = ttk.Treeview(frame2, columns=("date", "description", "income", "expense", "balance"), show="headings")

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

    table.pack(padx=10, pady=10)

    # table.insert("", index=ctk.END, values=("Abubakr", "Bardien", "abubakrbardien@gmail.com"))

    root.mainloop()

MainWindow()
