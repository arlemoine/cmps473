import tkinter as tk
import access
from tkinter import filedialog
from PIL import ImageTk # Needed for tkinter label compatibility
import process

class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Image Filtration")
        self.root.minsize(1200, 1000)
        # self.root.grid_rowconfigure(0, weight=1)
        # self.root.grid_columnconfigure(0, weight=1)
        self.kernelList = access.loadKernelList()

        # Create frames for window
        self.frameToolbar = tk.Frame(self.root, bg="lightblue")
        self.frameToolbar.grid(row=0, column=0, columnspan=4, padx=2, pady=2, sticky="nsew")
        self.frameImage = tk.Frame(self.root)
        self.frameImage.grid(row=1, column=0, rowspan=4, columnspan=3, padx=2, pady=2, sticky="nsew")
        self.frameHistory = tk.Frame(self.root, bg="darkgrey")
        self.frameHistory.grid(row=1, column=3, rowspan=4, padx=2, pady=2, sticky="nsew")
        self.frameData = tk.Frame(self.root, bg="darkgrey")
        self.frameData.grid(row=5, column=0, rowspan=2, columnspan=4, padx=2, pady=2, sticky="nsew")
        
        # Create kernel frame for kernel window
        self.frameKernel = tk.Frame(self.root)
        self.frameKernel.grid(row=1, column=0, columnspan=4, padx=2, pady=2, sticky="nsew")
        self.frameKernel.grid_forget() # Hides the kernel window during startup

        # Configure row and column weights to allow resizing
        self.root.grid_rowconfigure(0, weight=0)  # Toolbar row (non-resizable)
        self.root.grid_rowconfigure(1, weight=2)  # Image and history row 
        self.root.grid_rowconfigure(2, weight=2)  # Image and history row
        self.root.grid_rowconfigure(3, weight=2)  # Image and history row
        self.root.grid_rowconfigure(4, weight=2)  # Image and history row
        self.root.grid_rowconfigure(5, weight=2)  # Data row 
        self.root.grid_rowconfigure(6, weight=2)  # Data row

        self.root.grid_columnconfigure(0, weight=2)  # Image column
        self.root.grid_columnconfigure(1, weight=2)  # Image column 
        self.root.grid_columnconfigure(2, weight=2)  # Image column
        self.root.grid_columnconfigure(3, weight=2)  # History column

        # Track active frame
        self.frameActive = self.frameImage

        self.tkImage = None
        self.image = None

        # Set up frames
        self.setFrameToolbar()
        self.setFrameImage()
        self.setFrameHistory()
        self.setFrameData()
        self.setFrameKernel()

    def run(self):
        """Main loop to run the window."""
        self.root.mainloop()

    def toggleWindowKernel(self):
        if self.frameActive == self.frameImage:
            self.frameImage.grid_forget()
            self.frameHistory.grid_forget()
            self.frameData.grid_forget()
            self.frameKernel.grid(row=1, column=0, columnspan=4, padx=2, pady=2, sticky="nsew")
            self.frameActive = self.frameKernel
        elif self.frameActive == self.frameKernel:
            self.frameKernel.grid_forget()
            self.frameImage.grid(row=1, column=0, rowspan=4, columnspan=3, padx=2, pady=2, sticky="nsew")
            self.frameHistory.grid(row=1, column=3, rowspan=4, padx=2, pady=2, sticky="nsew")
            self.frameData.grid(row=5, column=0, rowspan=2, columnspan=4, padx=2, pady=2, sticky="nsew")
            self.frameActive = self.frameImage

    def setFrameToolbar(self):
        # Kernel default kernel dropdown variable
        self.kernelSelectedDefault = tk.StringVar()
        self.kernelSelectedDefault.set("Select Default Kernel")

        # Place buttons
        tk.Button(self.frameToolbar, text="Load Image", command=self.loadImage).grid(row=0, column=0, padx=4, pady=4, sticky="w")
        # tk.Button(self.frameToolbar, text="Apply Filter", command=self.applyKernelToImage).grid(row=0, column=3, padx=10, pady=5, sticky="w")
        tk.Button(self.frameToolbar, text="Edit Kernel", command=self.toggleWindowKernel).grid(row=0, column=1, padx=4, pady=4, sticky="w")

        # Dropdown for defaults
        self.dropdown = tk.OptionMenu(
                self.frameToolbar, 
                self.kernelSelectedDefault, 
                *self.kernelList.keys(),
                command=lambda _: self.applyKernel()
                )
        self.dropdown.grid(row=0, column=2, columnspan=3, padx=6, pady=6, sticky="nsew")


    def setFrameImage(self):
        # Ensures image label's row/column is stretchable
        self.frameImage.grid_rowconfigure(0, weight=1, minsize=1)
        self.frameImage.grid_columnconfigure(0, weight=1, minsize=1)

        # Image preview label
        self.imageLabel = tk.Label(self.frameImage, anchor="center", bg="lightgreen")
        self.imageLabel.grid(row=0, column=0, sticky="nsew")

        self.frameImage.grid_propagate(False)

    def setFrameHistory(self):
        self.frameHistory.configure(bg="darkgrey")

        self.frameHistory.grid_propagate(False)

    def setFrameData(self):
        self.frameData.configure(bg="darkgrey")

        self.frameData.grid_propagate(False)

    def setFrameKernel(self):
        tk.Button(self.frameKernel, text="Load Kernel", command=self.loadKernel).grid(row=0, column=0, padx=4, pady=4, sticky="w")

        # Save kernel
        tk.Button(self.frameKernel, text="Save Kernel", command=self.saveKernel).grid(row=1, column=0, padx=4, pady=4, sticky="w")
        self.kernelNameVar = tk.StringVar()
        self.kernelNameEntry = tk.Entry(self.frameKernel, textvariable=self.kernelNameVar)
        self.kernelNameEntry.grid(row=1, column=1, columnspan=2, padx=4, pady=4)

        # Kernel size entry
        tk.Button(self.frameKernel, text="Resize (odd number)", command=self.setKernelSize).grid(row=3, column=0, padx=4, pady=4, sticky="w")
        self.kernelSizeEntry = tk.Entry(self.frameKernel)
        self.kernelSizeEntry.grid(row=3, column=1, columnspan=2, padx=4, pady=4)

        # Kernel grid frame
        self.frameKernelEntries = tk.Frame(self.frameKernel)
        self.frameKernelEntries.grid(row=4, column=0, columnspan=3, padx=4, pady=4)

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

    def setKernelSize(self):
        try:
            size = int(self.kernelSizeEntry.get())
            if size % 2 == 0 or size < 1:
                raise ValueError("Must be odd and positive.")
            self.setKernelGrid(size)
        except ValueError as ve:
            print(f"Invalid kernel size: {ve}")

    def loadKernel(self):
        kernel = access.loadKernel()

        if kernel is not None:
            size = len(kernel)
            self.kernelSizeEntry.delete(0, tk.END)
            self.kernelSizeEntry.insert(0, str(size))
            self.setKernelGrid(size)

            for i in range(size):
                for j in range(size):
                    self.kernelEntries[i][j].delete(0, tk.END)
                    self.kernelEntries[i][j].insert(0, str(kernel[i][j]))
        else:
            print("Failed to load kernel.")

    def saveKernel(self):
        # Get the name from your GUI (e.g., from a text entry or another widget)
        name = self.kernelNameEntry.get()  # Adjust this depending on how you get the name

        # Get the matrix from the grid of entries
        matrix = self.getKernelValuesFromGrid()  # Assuming this function is already defined in window.py to pull the matrix

        if name and matrix:  # Ensure both name and matrix are not empty
            access.saveKernel(name, matrix)  # Call the function from access.py to save the kernel
        else:
            print("Invalid kernel data. Please ensure the name and matrix are filled in.")

        # Reload the kernel list
        self.kernelList = access.loadKernelList()

        menu = self.dropdown['menu']
        menu.delete(0, tk.END)
        for k in self.kernelList:
            menu.add_command(label=k, command=lambda val=k: option.set(val))
        

    def applyKernel(self):
        name = self.kernelSelectedDefault.get()
        if name not in self.kernelList:
            print("Invalid or no kernel selected.")
            return

        default = self.kernelList[name]
        size = len(default)

        self.kernelSizeEntry.delete(0, tk.END)
        self.kernelSizeEntry.insert(0, str(size))
        self.setKernelGrid(size)

        for i in range(size):
            for j in range(size):
                self.kernelEntries[i][j].delete(0, tk.END)
                self.kernelEntries[i][j].insert(0, str(default[i][j]))

    def getKernelValuesFromGrid(self):
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

        kernel = self.getKernelValuesFromGrid()
        result = process.applyKernelToImage(self.image, kernel)

        self.tkImage = access.prepImageForWindow(result)
        self.imageLabel.config(image=self.tkImage)
        self.image = result # Store updated version

if __name__ == "__main__":
    default = Window()
    default.run()
