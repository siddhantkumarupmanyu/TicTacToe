import tkinter as tk

def pack():
    window = tk.Tk()

    frame1 = tk.Frame(master=window, height=100, bg="red")
    frame1.pack(fill=tk.X)

    frame2 = tk.Frame(master=window, height=50, bg="yellow")
    frame2.pack(fill=tk.X)

    frame3 = tk.Frame(master=window, height=25, bg="blue")
    frame3.pack(fill=tk.X)

    window.mainloop()

def packVertical():
    window = tk.Tk()

    frame1 = tk.Frame(master=window, width=200, height=100, bg="red")
    frame1.pack(fill=tk.Y, side=tk.LEFT)

    frame2 = tk.Frame(master=window, width=100, bg="yellow")
    frame2.pack(fill=tk.Y, side=tk.LEFT)

    frame3 = tk.Frame(master=window, width=50, bg="blue")
    frame3.pack(fill=tk.Y, side=tk.LEFT)

    window.mainloop()

def packResponsive():
    window = tk.Tk()

    frame1 = tk.Frame(master=window, width=200, height=100, bg="red")
    frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    frame2 = tk.Frame(master=window, width=100, bg="yellow")
    frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    frame3 = tk.Frame(master=window, width=50, bg="blue")
    frame3.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

    window.mainloop()