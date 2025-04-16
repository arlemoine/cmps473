from tkinter import *
from tkinter import ttk
from tkinter import font

class FeetToMeters:

    def __init__(self, root):

        root.title("Feet to Meters")

        font_style = ("Helvetica", 16)

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        for i in range(1, 4):
            mainframe.columnconfigure(i, weight=1)
        for i in range(1, 4):
            mainframe.rowconfigure(i, weight=1)

        self.feet = StringVar()
        feet_entry = Entry(mainframe, width=15, textvariable=self.feet, font=font_style)
        feet_entry.grid(column=2, row=1, sticky=(W, E))
        self.meters = StringVar()

        ttk.Label(mainframe, textvariable=self.meters, font=font_style).grid(column=2, row=2, sticky=(W, E))
        ttk.Button(mainframe, text="Calculate", command=self.calculate).grid(column=3, row=3, sticky=W)

        ttk.Label(mainframe, text="feet", font=font_style).grid(column=3, row=1, sticky=W)
        ttk.Label(mainframe, text="is equivalent to", font=font_style).grid(column=1, row=2, sticky=E)
        ttk.Label(mainframe, text="meters", font=font_style).grid(column=3, row=2, sticky=W)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        feet_entry.focus()
        root.bind("<Return>", self.calculate)

    def calculate(self, *args):
        try:
            value = float(self.feet.get())
            self.meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0)
        except ValueError:
            pass

root = Tk()
FeetToMeters(root)
root.mainloop()
