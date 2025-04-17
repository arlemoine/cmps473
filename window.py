import tkinter as tk
import access
from tkinter import filedialog
from PIL import ImageTk # Needed for tkinter label compatibility
import process

class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Filtration")
        self.root.minsize(800, 600)
        self.kernelDefaults = access.loadKernelList()

        # Create frames for window
        self.frameMain = tk.Frame(self.root)
        self.frameMain.grid(row=0, column=0, sticky="nsew")
        self.frameInput = tk.Frame(self.root)
        self.frameInput.grid(row=0, column=0, sticky="nsew")
        self.frameInput.grid_remove() #Start hidden
        self.frameDisplay = tk.Frame(self.root)
        self.frameDisplay.grid(row=0, column=0, sticky="nsew")
        self.frameDisplay.grid_remove() # Start hidden

        # Track active frame
        self.frameActive = self.frameMain

        self.tkImage = None
        self.image = None

        # GUI components
        self.setMainFrame()
        self.setInputFrame()

    def run(self):
        """Main loop to run the window."""
        self.root.mainloop()

    def switchFrame(self, frameTarget):
        if self.frameActive is not None:
            self.frameActive.grid_remove()
        frameTarget.grid()
        self.frameActive = frameTarget

    def setMainFrame(self):
        tk.Button(self.frameMain, text="Input", command=lambda: self.switchFrame(self.frameInput)).grid(padx=10, pady=5)

    def setInputFrame(self):
        # Kernel default kernel dropdown variable
        self.kernelSelectedDefault = tk.StringVar()
        self.kernelSelectedDefault.set("Select Default Kernel")

        # Buttons
        tk.Button(self.frameInput, text="Load Image", command=self.loadImage).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        tk.Button(self.frameInput, text="Set Kernel Size", command=self.setKernelFields).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        tk.Button(self.frameInput, text="Apply Filter", command=self.applyKernelToImage).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        tk.Button(self.frameInput, text="Save Kernel").grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # Image preview label
        self.imageLabel = tk.Label(self.frameInput)
        self.imageLabel.grid(row=1, column=3, columnspan=3, rowspan=3, padx=10, pady=5, sticky="e")

        # Dropdown for defaults
        dropdown = tk.OptionMenu(
                self.frameInput, 
                self.kernelSelectedDefault, 
                *self.kernelDefaults.keys(),
                command=lambda _: self.applyDefaultKernel()
                )
        dropdown.grid(row=1, column=0, columnspan=3, padx=10, pady=5, sticky="ew")

        # Kernel size entry
        self.kernelSizeEntry = tk.Entry(self.frameInput)
        self.kernelSizeEntry.grid(row=3, column=1, columnspan=2, padx=10, pady=5)

        # Kernel name entry
        self.kernelNameVar = tk.StringVar()
        self.kernelNameEntry = tk.Entry(self.frameInput, textvariable=self.kernelNameVar)
        self.kernelNameEntry.grid(row=2, column=1, columnspan=2, padx=10, pady=5)

        # Kernel grid frame
        self.frameKernelEntries = tk.Frame(self.frameInput)
        self.frameKernelEntries.grid(row=3, column=0, columnspan=3, padx=10, pady=5)

    def setKernelGrid(self, size):
        for widget in self.frameKernelEntries.winfo_children():
            widget.destroy()
        self.kernelEntries = []
        for i in range(size):
            row = []
            for j in range(size):
                entry = tk.Entry(self.frameKernelEntries, width=5)
                entry.grid(row=i, column=j)
                row.append(entry)
            self.kernelEntries.append(row)

    def setKernelFields(self):
        try:
            size = int(self.kernelSizeEntry.get())
            if size % 2 == 0 or size < 1:
                raise ValueError("Must be odd and positive.")
            self.setKernelGrid(size)
        except ValueError as ve:
            print(f"Invalid kernel size: {ve}")

    def applyDefaultKernel(self):
        name = self.kernelSelectedDefault.get()
        if name not in self.kernelDefaults:
            print("Invalid or no kernel selected.")
            return

        default = self.kernelDefaults[name]
        size = len(default)

        self.kernelSizeEntry.delete(0, tk.END)
        self.kernelSizeEntry.insert(0, str(size))
        self.setKernelGrid(size)

        for i in range(size):
            for j in range(size):
                self.kernelEntries[i][j].delete(0, tk.END)
                self.kernelEntries[i][j].insert(0, str(default[i][j]))

    def readKernel(self):
        kernel = []
        for row in self.kernelEntries:
            kernelRow = []
            for entry in row:
                try:
                    val = float(entry.get())
                except ValueError:
                    val = 0.0
                kernelRow.append(val)
            kernel.append(kernelRow)
        print("Kernel:", kernel)
        return kernel

    def loadImage(self):
        filepath = filedialog.askopenfilename()
        if filepath:
            self.image = access.loadImage(filepath)
            self.tkImage = access.prepImageForWindow(self.image)
            if self.tkImage:
                self.imageLabel.config(image=self.tkImage, text="")
            else:
                self.imageLabel.config(text="Failed to load image.")

    def applyKernelToImage(self):
        if self.image is None:
            print("No image loaded.")
            return

        kernel = self.readKernel()
        result = process.applyKernelToImage(self.image, kernel)

        self.tkImage = access.prepImageForWindow(result)
        self.imageLabel.config(image=self.tkImage)
        self.image = result # Store updated version

if __name__ == "__main__":
    default = Window()
    default.run()
