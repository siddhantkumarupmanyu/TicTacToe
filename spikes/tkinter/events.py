import tkinter as tk
import random


def keyEvent():
    window = tk.Tk()

    def handle_keypress(event):
        """Print the character associated to the key pressed"""
        print(event.char)

    # Bind keypress event to handle_keypress()
    window.bind("<Key>", handle_keypress)

    def handle_click(event):
        print("The button was clicked!")

    button = tk.Button(text="Click me!")
    button.bind("<Button-1>", handle_click)
    button.pack()
    window.mainloop()


def buttonCommand():
    def increase():
        value = int(lbl_value["text"])
        lbl_value["text"] = f"{value + 1}"

    def decrease():
        value = int(lbl_value["text"])
        lbl_value["text"] = f"{value - 1}"

    window = tk.Tk()

    window.rowconfigure(0, minsize=50, weight=1)
    window.columnconfigure([0, 1, 2], minsize=50, weight=1)

    btn_decrease = tk.Button(master=window, text="-", command=decrease)
    btn_decrease.grid(row=0, column=0, sticky="nsew")

    lbl_value = tk.Label(master=window, text="0")
    lbl_value.grid(row=0, column=1)

    btn_increase = tk.Button(master=window, text="+", command=increase)
    btn_increase.grid(row=0, column=2, sticky="nsew")

    window.mainloop()

def diceRoll():
    def roll():
        lbl_result["text"] = str(random.randint(1, 6))

    window = tk.Tk()
    window.columnconfigure(0, minsize=150)
    window.rowconfigure([0, 1], minsize=50)

    btn_roll = tk.Button(text="Roll", command=roll)
    lbl_result = tk.Label()

    btn_roll.grid(row=0, column=0, sticky="nsew")
    lbl_result.grid(row=1, column=0)

    window.mainloop()
