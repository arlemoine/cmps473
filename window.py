import tkinter as tk
import access
from tkinter import filedialog
from PIL import ImageTk # Needed for tkinter label compatibility
import process

class Window:
    def __init__(self):
        # Configure root frame
        self.root = tk.Tk()
        self.root.title("Image Filtration")
        self.root.minsize(1200, 1000)

        self.kernelList = access.loadKernelList()
        self.kernelMatrixEntries = []
        self.history = [] # List of PIL Images
        self.historyThumbnails = []
        self.displayedImage = None
        self.image = None

        # Create frames
        self.frameToolbar = tk.Frame(self.root, name="frameToolbar", bg="lightblue")
        self.frameImage = tk.Frame(self.root, name="frameImage")
        self.frameHistory = tk.Frame(self.root, name="frameHistory", bg="darkgrey")
        self.frameData = tk.Frame(self.root, name="frameData", bg="darkgrey")
        self.frameKernel = tk.Frame(self.root, name="frameKernel")
        
        # Place frames
        self.frameToolbar.grid(row=0, column=0, columnspan=4, padx=2, pady=2, sticky="nsew")
        self.frameImage.grid(row=1, column=0, rowspan=4, columnspan=3, padx=2, pady=2, sticky="nsew")
        self.frameHistory.grid(row=1, column=3, rowspan=4, padx=2, pady=2, sticky="nsew")
        self.frameData.grid(row=5, column=0, rowspan=2, columnspan=4, padx=2, pady=2, sticky="nsew")
        self.frameKernel.grid(row=1, column=0, columnspan=4, padx=2, pady=2, sticky="nsew")

        # Hide frames which are not part of the main window
        self.frameKernel.grid_forget() # Hides the kernel window during startup

        # Configure row and column weights to control resizing
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
        self.frameActive = self.frameImage # Track active frame for switching

        # Set up frames
        self.setFrameToolbar()
        self.setFrameImage()
        self.setFrameHistory()
        self.setFrameData()
        self.setFrameKernel()

    def run(self):
        """Start the Tkinter main event loop to display the GUI."""
        self.root.mainloop()


    def setFrameToolbar(self):
        """Create and configure the top toolbar frame with buttons and dropdown."""
        # Kernel kernel dropdown selection dropdown variable
        self.kernelDropdownSelection = tk.StringVar()
        self.kernelDropdownSelection.set("Select Default Kernel")

        # Place buttons
        tk.Button(self.frameToolbar, text="Load Image", command=self.loadImage).grid(row=0, column=0, padx=4, pady=4, sticky="w")
        tk.Button(self.frameToolbar, text="Apply Filter", command=self.applyKernelToImage).grid(row=0, column=1, padx=10, pady=5, sticky="w")
        tk.Button(self.frameToolbar, text="Edit Kernel", command=self.toggleWindowKernel).grid(row=0, column=5, padx=4, pady=4, sticky="w")

        # Dropdown for defaults
        self.kernelDropdown = tk.OptionMenu(
                self.frameToolbar, 
                self.kernelDropdownSelection, 
                *self.kernelList.keys(),
                command=lambda _: self.updateSelectedKernel()
                )
        self.kernelDropdown.grid(row=0, column=2, columnspan=3, padx=6, pady=6, sticky="nsew")

        print("Toolbar frame initialized.")

    def setFrameImage(self):
        """Create the frame for displaying the image and configure resizing behavior."""
        # Ensures image label's row/column is stretchable
        self.frameImage.grid_rowconfigure(0, weight=1, minsize=1)
        self.frameImage.grid_columnconfigure(0, weight=1, minsize=1)

        # Image preview label
        self.imageLabel = tk.Label(self.frameImage, anchor="center", bg="lightgreen")
        self.imageLabel.grid(row=0, column=0, sticky="nsew")

        self.frameImage.grid_propagate(False)

        print("Image frame initialized.")

    def setFrameHistory(self):
        """Create the frame for displaying the filter history (currently placeholder)."""
        self.frameHistory.configure(bg="darkgrey")

        self.frameHistory.grid_propagate(False)

        print("History frame initialized.")

    def setFrameData(self):
        """Create the frame for displaying image data or stats (currently placeholder)."""
        self.frameData.configure(bg="darkgrey")

        self.frameData.grid_propagate(False)

        print("Data frame initialized.")

    def setFrameKernel(self):
        """Set up the UI elements for the kernel editing interface."""
        # Save kernel
        tk.Button(self.frameKernel, text="Save Kernel", command=self.saveKernel).grid(row=0, column=0, padx=4, pady=4, sticky="w")
        self.kernelNameVar = tk.StringVar()
        self.kernelNameEntry = tk.Entry(self.frameKernel, textvariable=self.kernelNameVar)
        self.kernelNameEntry.grid(row=0, column=1, columnspan=2, padx=4, pady=4)

        # Kernel size entry
        tk.Button(self.frameKernel, text="Resize (odd number)", command=self.getKernelSizeFromUI).grid(row=1, column=0, padx=4, pady=4, sticky="w")
        self.kernelSizeEntry = tk.Entry(self.frameKernel)
        self.kernelSizeEntry.grid(row=1, column=1, columnspan=2, padx=4, pady=4)

        # Kernel grid frame
        self.kernelNameLabel = tk.Label(self.frameKernel, text="Kernel Matrix") 
        self.kernelNameLabel.grid(row=2, column=0, columnspan=3, padx=4, pady=4)
        self.frameKernelMatrix = tk.Frame(self.frameKernel)
        self.frameKernelMatrix.grid(row=3, column=0, columnspan=3, padx=4, pady=4, sticky="nw")

        print("Kernel frame initialized.")

    def toggleWindowKernel(self):
        """Toggle between the main image view and the kernel editing view."""
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
            self.frameImage.grid_propagate(False)
            self.frameHistory.grid_propagate(False)
            self.frameData.grid_propagate(False)

        print(f"Current window -> {self.frameActive.winfo_name()}")

    def setKernelGrid(self, size):
        """
        Create a grid of Entry widgets for editing kernel values.
        Args:
            size (int): The size of the kernel (must be odd).
        """
        # Destroy old entry matrix and clear out old references in the matrix entry list
        for widget in self.frameKernelMatrix.winfo_children():
            widget.destroy()
        self.kernelMatrixEntries.clear()

        # Create new grid
        for i in range(size):
            row = []
            for j in range(size):
                entry = tk.Entry(self.frameKernelMatrix, width=5)
                entry.grid(row=i, column=j)
                row.append(entry)
            self.kernelMatrixEntries.append(row)

        print(f"Set kernel matrix to size {size}x{size}")

    def getKernelSizeFromUI(self):
        """
        Read size from entry and update the kernel grid. Validates that the entered size is a positive odd integer.
        """
        try:
            size = int(self.kernelSizeEntry.get())
            if size % 2 == 0 or size < 1:
                raise ValueError("Must be odd and positive.")
            self.setKernelGrid(size)
        except ValueError as ve:
            print(f"Invalid kernel size: {ve}")

        print(f"Retrieved kernel size: {size}")

    def saveKernel(self):
        """
        Save the current kernel grid values to a JSON file. Requires the user to enter a kernel name.
        """
        # Get name and matrix from GUI, pass to access.py for saving
        name = self.kernelNameEntry.get() 
        matrix = self.getMatrixFromUI() 

        if name and matrix:  # Ensure both name and matrix are not empty
            access.saveKernel(name, matrix)  # Call the function from access.py to save the kernel
        else:
            print("Invalid kernel data. Please ensure the name and matrix are filled in.")

        self.updateKernelList()

    def updateKernelList(self):
        """
        Update the kernel list as well as the dropdown menu holding the list.
        """
        # Reload the kernel list
        self.kernelList = access.loadKernelList()
        print("Kernel list reloaded")
        
        # Update the dropdown menu for the kernel list
        menu = self.kernelDropdown['menu']
        menu.delete(0, tk.END)
        for k in self.kernelList:
            menu.add_command(
                label=k,
                command=lambda val=k: [
                    self.kernelDropdownSelection.set(val),
                    self.updateSelectedKernel()
                ]
            )
        print("Dropdown box reloaded.")

    def updateSelectedKernel(self):
        """
        Get info of kernel selected in kernel selection dropdown and update the kernel frame.
        """
        # Get selected kernel name and matrix size
        name = self.kernelDropdownSelection.get()
        matrix = self.kernelList[name]
        size = len(matrix)

        # Update kernel name entry box
        self.kernelNameVar.set(name)

        # Update kernel size entry box
        self.kernelSizeEntry.delete(0, tk.END)
        self.kernelSizeEntry.insert(0, str(size))
        self.setKernelGrid(size)

        # Update kernel matrix field
        for i in range(size):
            for j in range(size):
                self.kernelMatrixEntries[i][j].delete(0, tk.END)
                self.kernelMatrixEntries[i][j].insert(0, str(matrix[i][j]))

    def getMatrixFromUI(self):
        """
        Retrieve kernel values from the entry grid.
        Returns:
            2D array representing kernel matrix
        """
        kernel = []
        for row in self.kernelMatrixEntries:
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
        """
        Open a file dialog to load an image from disk. Converts and displays the image in the preview frame.
        """
        filepath = filedialog.askopenfilename()
        if filepath:
            self.image = access.loadImage(filepath)
            self.displayedImage = access.prepImageForWindow(self.image)
            if self.displayedImage:
                self.imageLabel.config(image=self.displayedImage, text="")
            else:
                self.imageLabel.config(text="Failed to load image.")

    def applyKernelToImage(self):
        """
        Use current kernel to perform image filtration and update the displayed image.
        """
        # Ensure image exists prior to filtration
        if self.image is None:
            print("No image loaded.")
            return

        kernel = self.getMatrixFromUI()
        resultingImage = process.applyKernelToImage(self.image, kernel)
        self.displayedImage = access.prepImageForWindow(resultingImage) # Create thumbnail to be displayed
        self.imageLabel.config(image=self.displayedImage)
        self.image = resultingImage # Store updated image

        print("Image processing complete.")

if __name__ == "__main__":
    default = Window()
    default.run()
