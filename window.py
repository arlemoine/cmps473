import tkinter as tk
import imgAccess
from tkinter import filedialog
from PIL import ImageTk # Needed for tkinter label compatibility
import imgProc

class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Filtration")
        self.root.minsize(800, 600)
        self.kernelDefaults = {
            "Gaussian Blur 3x3": [
                [1, 2, 1],
                [2, 4, 2],
                [1, 2, 1]
            ],
            "Gaussian Blur 5x5": [
                [1, 4, 7, 4, 1],
                [4, 16, 26, 16, 4],
                [7, 26, 41, 26, 7],
                [4, 16, 26, 16, 4],
                [1, 4, 7, 4, 1]
            ],
            "Edge Detect 3x3": [
                [-1, -1, -1],
                [-1, 8, -1],
                [-1, -1, -1]
            ],
            "Sharpen 3x3": [
                [0, -1, 0],
                [-1, 5, -1],
                [0, -1, 0]
            ],
            "Box Blur 3x3": [
                [1/9]*3,
                [1/9]*3,
                [1/9]*3
            ]
        }

        # Create frames for window
        self.frameMain = tk.Frame(self.root)
        self.frameMain.pack(padx=10, pady=5)
        self.frameInput = tk.Frame(self.root)
        self.frameInput.pack(padx=10, pady=5)
        self.frameInput.pack_forget() #Start hidden
        self.frameDisplay = tk.Frame(self.root)
        self.frameDisplay.pack(padx=10, pady=5)
        self.frameDisplay.pack_forget() # Start hidden

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
            self.frameActive.pack_forget()
        frameTarget.pack(padx=10, pady=5)
        self.frameActive = frameTarget

    def setMainFrame(self):
        tk.Button(self.frameMain, text="Input", command=lambda: self.switchFrame(self.frameInput)).pack(padx=10, pady=5)

    def setInputFrame(self):
        # Kernel default kernel dropdown variable
        self.kernelSelectedDefault = tk.StringVar()
        self.kernelSelectedDefault.set("Select Default Kernel")

        tk.Button(self.frameInput, text="Load Image", command=self.loadImage).pack(padx=10, pady=5)

        # Image preview label
        self.imageLabel = tk.Label(self.frameInput)
        self.imageLabel.pack(padx=10, pady=5)

        # Dropdown for defaults
        dropdown = tk.OptionMenu(
                self.frameInput, 
                self.kernelSelectedDefault, 
                *self.kernelDefaults.keys(),
                command=lambda _: self.applyDefaultKernel()
                )
        dropdown.pack(padx=10, pady=5)

        # Kernel size entry
        self.kernelSizeEntry = tk.Entry(self.frameInput)
        self.kernelSizeEntry.pack(padx=10, pady=5)

        # Kernel grid frame
        self.frameKernelEntries = tk.Frame(self.frameInput)
        self.frameKernelEntries.pack(padx=10, pady=5)

        tk.Button(self.frameInput, text="Set Kernel Size", command=self.setKernelFields).pack(padx=10, pady=5)
        tk.Button(self.frameInput, text="Apply Filter", command=self.applyKernelToImage).pack(padx=10, pady=5)

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
            self.image = imgAccess.loadImage(filepath)
            self.tkImage = imgAccess.prepImageForWindow(self.image)
            if self.tkImage:
                self.imageLabel.config(image=self.tkImage, text="")
            else:
                self.imageLabel.config(text="Failed to load image.")

    def applyKernelToImage(self):
        if self.image is None:
            print("No image loaded.")
            return

        kernel = self.readKernel()
        result = imgProc.applyKernelToImage(self.image, kernel)

        self.tkImage = imgAccess.prepImageForWindow(result)
        self.imageLabel.config(image=self.tkImage)
        self.image = result # Store updated version

if __name__ == "__main__":
    default = Window()
    default.run()
