import tkinter as tk

#### NOTES ####
# width and height are measured in text units
# One horizontal text unit is determined by the width of the character "0",
# or the number zero, in the default system font.
# Similarly, one vertical text unit is determined by the height of the character "0".
from spikes.tkinter.GeometryManager.grid import gridSticky, grid
from spikes.tkinter.address_form import createAddressFormShort
from spikes.tkinter.events import keyEvent, buttonCommand, diceRoll
from spikes.tkinter.temperatue_converter import runFahrenheit
from spikes.tkinter.text_editor import simpleEditor


def run():
    window = tk.Tk()
    label = tk.Label(
        text="Hello, Tkinter",
        fg="white",
        bg="black",
        width=11,
        height=10
    )
    button = tk.Button(
        text="Click me!",
        width=25,
        height=5,
        bg="blue",
        fg="yellow",
    )
    entry = tk.Entry(fg="yellow", bg="blue", width=50)
    label.pack()
    button.pack()
    entry.pack()
    window.mainloop()


if __name__ == '__main__':
    # run()
    # entry()
    # frame()
    # frameReliefs()
    # pack()
    # packVertical()
    # packResponsive()
    # place()
    grid()
    # gridSticky()
    # createAddressForm()
    # createAddressFormShort()
    # keyEvent()
    # buttonCommand()
    # diceRoll()
    # runFahrenheit()
    # simpleEditor()