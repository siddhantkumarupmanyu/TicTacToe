import tkinter as tk


def entry():
    window = tk.Tk()
    label = tk.Label(text="Name")
    entry = tk.Entry()
    label.pack()
    entry.pack()
    window.mainloop()
