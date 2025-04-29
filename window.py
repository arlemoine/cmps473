import tkinter as tk
import access
from tkinter import filedialog
from PIL import ImageTk # Needed for tkinter label compatibility
import process
import ttkbootstrap as tb
from ttkbootstrap.tooltip import ToolTip

class Window:
    def __init__(self):
        # Configure root frame
        self.root = tb.Window(themename="cosmo")
        self.root.title("Image Filtration")
        self.root.minsize(1200, 1000)

        # Configure grid of root
        self.root.grid_rowconfigure(1, weight=1) # Row of image panel
        self.root.grid_columnconfigure(0, weight=1) # Column of image panel

        self.createFrames()
        
        # Main variables
        self.kernelList = access.loadKernelList()
        self.kernelMatrixEntries = []
        self.history = [] # List of PIL Images
        self.historyThumbnails = []
        self.imageThumbnail = None
        self.image = None
        self.historyToggle = False
        self.medianSize=[3, 5, 7, 9, 11, 13, 15, 17, 19, 21]

        self.setWindowMain()
        self.frameActive = self.frameImage # Track active frame for switching

        # Set up frames
        self.definePanelToolbar()
        self.definePanelImage()
        self.definePanelHistory()
        self.definePanelData()
        self.defineWindowKernel()

    def run(self):
        """Start the Tkinter main event loop to display the GUI."""
        self.root.mainloop()

    def createFrames(self):
        # Create frames
        self.frameToolbar = tb.Frame(self.root, name="frameToolbar", bootstyle="dark")
        self.frameImage = tb.Frame(self.root, name="frameImage", bootstyle="dark")
        self.frameHistory = tb.Frame(self.root, name="frameHistory", width=100, bootstyle="dark")
        self.frameData = tb.Frame(self.root, name="frameData", height=300, bootstyle="dark")
        self.frameKernel = tb.Frame(self.root, name="frameKernel", bootstyle="dark")

    def setWindowMain(self):
        """Switch active window to main window."""
        # Hide irrelevant frames
        self.frameKernel.grid_forget() # Hides the kernel window during startup

        # Expose relevant frames
        self.frameToolbar.grid(row=0, column=0, columnspan=6, padx=2, pady=2, sticky="nsew")
        self.frameImage.grid(row=1, column=0, rowspan=4, columnspan=5, padx=2, pady=2, sticky="nsew")
        self.frameHistory.grid(row=1, column=5, rowspan=4, padx=2, pady=2, sticky="nsew")
        self.frameData.grid(row=5, column=0, rowspan=2, columnspan=6, padx=2, pady=2, sticky="nsew")

        # Control propagation of frames
        self.frameImage.grid_propagate(False)
        self.frameHistory.grid_propagate(False)
        self.frameData.pack_propagate(False)
        
    def setWindowKernel(self):
        """Switch active window to kernel window."""
        # Hide irrelevant frames
        self.frameImage.grid_forget()
        self.frameHistory.grid_forget()
        self.frameData.grid_forget()

        # Expose relevant frames
        self.frameKernel.grid(row=1, column=0, columnspan=4, padx=2, pady=2, sticky="nsew")

    def definePanelToolbar(self):
        """Configure the top toolbar frame with buttons and dropdown."""
        # Kernel kernel dropdown selection dropdown variable
        self.kernelDropdownSelection = tk.StringVar()
        self.kernelDropdownSelection.set("Kernel Selection")
        self.medianNeighborSize = tk.StringVar()
        self.medianNeighborSize.set("Median Size")

        # Icons
        self.iconLoad = tk.PhotoImage(file="resources/load.png")
        self.iconSave = tk.PhotoImage(file="resources/save.png")
        self.iconCompare = tk.PhotoImage(file="resources/compare.png")
        self.iconConvolution = tk.PhotoImage(file="resources/convolution.png")
        self.iconMedianFilter = tk.PhotoImage(file="resources/medianFilter.png")
        self.iconHist = tk.PhotoImage(file="resources/equalize.png")

        # Separators
        self.separator1 = tb.Separator(self.frameToolbar, orient="vertical")
        self.separator2 = tb.Separator(self.frameToolbar, orient="vertical")
        self.separator3 = tb.Separator(self.frameToolbar, orient="vertical")

        # Create buttons
        self.buttonLoad = tb.Button(self.frameToolbar, bootstyle="light", image=self.iconLoad, command=self.loadImage)
        self.buttonSave = tb.Button(self.frameToolbar, bootstyle="light", image=self.iconSave, command=self.saveImage)
        self.buttonConvulge = tb.Button(self.frameToolbar, bootstyle="light", image=self.iconConvolution, command=self.applyKernelToImage)
        self.buttonKernelEdit = tb.Button(self.frameToolbar, bootstyle="dark-link", text="Edit Kernel", command=self.toggleWindowKernel)
        self.buttonHistEqualization = tb.Button(self.frameToolbar, bootstyle="light", image=self.iconHist, command=self.applyEqualization)
        self.buttonCompare = tb.Button(self.frameToolbar, bootstyle="light", image=self.iconCompare, command=self.toggleOriginalImage)
        self.buttonMedianFilter = tb.Button(self.frameToolbar, bootstyle="light", image=self.iconMedianFilter, command=self.applyMedianFilter)

        # Create kernel list dropdown
        self.kernelDropdown = tb.OptionMenu(
            self.frameToolbar, 
            self.kernelDropdownSelection, 
            bootstyle="light",
            *self.kernelList.keys(),
            command=lambda _: self.updateSelectedKernel()
            )
        self.medianSizeDropdown = tb.OptionMenu(
                    self.frameToolbar, 
                    self.medianNeighborSize, 
                    bootstyle="light",
                    *self.medianSize
                    )
       # self.medianSizeEntry = tb.Entry(self.frameToolbar, bootstyle="light", textvariable=self.medianNeighborSize)

        # Place widgets
        self.buttonLoad.pack(side="left", padx=6, pady=6)
        self.buttonSave.pack(side="left", padx=6, pady=6)
        self.separator1.pack(side="left", fill="x", padx=10)
        self.buttonCompare.pack(side="left", padx=6, pady=6)
        self.buttonHistEqualization.pack(side="left", padx=6, pady=6)
        self.separator2.pack(side="left", fill="x", padx=10)
        self.buttonMedianFilter.pack(side="left", padx=6, pady=6)
        self.medianSizeDropdown.pack(side="left", padx=6, pady=6)
        self.separator3.pack(side="left", fill="x", padx=10)
        self.buttonConvulge.pack(side="left", padx=6, pady=6)
        self.kernelDropdown.pack(side="left", padx=6, pady=6)
        self.buttonKernelEdit.pack(side="left", padx=6, pady=6)

        print("Toolbar frame initialized.")

    def definePanelImage(self):
        """Configure the frame for displaying the image and configure resizing behavior."""
        # Ensures image label's row/column is stretchable
        self.frameImage.grid_rowconfigure(0, weight=1, minsize=1)
        self.frameImage.grid_columnconfigure(0, weight=1, minsize=1)

        # Image preview label
        self.imageLabel = tb.Label(self.frameImage, anchor="center", bootstyle="dark")
        self.imageLabel.grid(row=0, column=0, padx=8, pady=8, sticky="nsew")

        print("Image frame initialized.")

    def definePanelHistory(self):
        """Configure the frame for displaying the filter history (currently placeholder)."""
        # Create Canvas widget to hold content as well as the scrollbar and scrollframe to allow for scrolling
        self.historyCanvas = tk.Canvas(self.frameHistory, width=260, highlightthickness=0)
        self.historyScrollbar = tk.Scrollbar(self.frameHistory, orient="vertical", width=20, command=self.historyCanvas.yview)
        self.historyScrollFrame = tk.Frame(self.historyCanvas)

        self.historyScrollFrame.bind(
            "<Configure>",
            lambda e: self.historyCanvas.configure(scrollregion=self.historyCanvas.bbox("all"))
        )

        self.historyCanvas.create_window((0,0), window=self.historyScrollFrame, anchor="nw")
        self.historyCanvas.configure(yscrollcommand=self.historyScrollbar.set)

        self.historyCanvas.pack(side="left", fill="both", expand=True)
        self.historyScrollbar.pack(side="right", fill="both")

        print("History frame initialized.")

    def definePanelData(self):
        """Configure the frame for displaying image data or stats (currently placeholder)."""
        # Create a placeholder for the histogram
        self.histLabel = tb.Label(self.frameData, anchor="center", bootstyle="inverse")
        self.histLabel.pack(fill="both", expand=True)

        print("Data frame initialized.")

    def defineWindowKernel(self):
        """Configure the UI elements for the kernel editing interface."""
        # Save kernel
        tb.Button(self.frameKernel, text="Save Kernel", bootstyle="success-outline", command=self.saveKernel).grid(row=0, column=0, padx=4, pady=4, sticky="w")
        self.kernelNameVar = tk.StringVar()
        self.kernelNameEntry = tk.Entry(self.frameKernel, textvariable=self.kernelNameVar)
        self.kernelNameEntry.grid(row=0, column=1, columnspan=2, padx=4, pady=4)

        # Kernel size entry
        tb.Button(self.frameKernel, text="Resize (odd number)", bootstyle="success-outline", command=self.getKernelSizeFromUI).grid(row=1, column=0, padx=4, pady=4, sticky="w")
        self.kernelSizeEntry = tb.Entry(self.frameKernel)
        self.kernelSizeEntry.grid(row=1, column=1, columnspan=2, padx=4, pady=4)

        # Kernel grid frame
        self.kernelNameLabel = tb.Label(self.frameKernel, text="Kernel Matrix", bootstyle="inverse") 
        self.kernelNameLabel.grid(row=2, column=0, columnspan=3, padx=4, pady=4)
        self.frameKernelMatrix = tb.Frame(self.frameKernel, bootstyle="dark")
        self.frameKernelMatrix.grid(row=3, column=0, columnspan=3, padx=4, pady=4, sticky="nw")

        print("Kernel frame initialized.")

    def toggleWindowKernel(self):
        """Toggle between the main image view and the kernel editing view."""
        if self.frameActive == self.frameImage:
            self.setWindowKernel()
            self.frameActive = self.frameKernel
        elif self.frameActive == self.frameKernel:
            self.setWindowMain()
            self.frameActive = self.frameImage
            
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

    def updateHistoryThumbnails(self):
        """Render thumbnail buttons in the scrollable history panel."""
        for widget in self.historyScrollFrame.winfo_children():
            widget.destroy()
        self.historyThumbnails.clear()

        for i, img in enumerate(self.history):
            thumb = img.copy()
            thumb.thumbnail((256, 256))
            thumbTk = ImageTk.PhotoImage(thumb)
            self.historyThumbnails.append(thumbTk)

            btn = tb.Button(self.historyScrollFrame, bootstyle="dark", image=thumbTk, command=lambda i=i: self.restoreHistory(i))
            btn.pack()

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
            colorImage = access.loadImage(filepath)
            grayscaleImage = process.grayscale(colorImage)
            self.updateImage(grayscaleImage)

    def loadHist(self):
        filepath = "temp/hist.png"
        if filepath:
            pilImage = access.loadImage(filepath)
            self.histImage = ImageTk.PhotoImage(pilImage) # Convert to PhotoImage
            self.histLabel.config(image=self.histImage, text="")
            print("Histogram loaded.")
        else:
            print("Histogram image could not be found.")

    def saveImage(self):
        access.saveImage(self.image)

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
        self.updateImage(resultingImage)
        print("Image processing complete.")

    def getHist(self):
        process.saveHistogram(self.image)
        self.loadHist()

    def restoreHistory(self, index):
        """Restore an image from the history and update the displayed image."""
        # Ensure the index is valid
        if 0 <= index < len(self.history):
            # Restore the image from the history at the given index
            previousImage = self.history[index]
            self.updateImage(previousImage, False)
            self.histIndexPointer = index
            print(f"Restored image from history at index {index}.")
        else:
            print("Invalid history index.")

    def applyEqualization(self):
        resultingImage = process.applyHistEq(self.image)
        self.updateImage(resultingImage)

    def applyMedianFilter(self):
        size = int(self.medianNeighborSize.get())
        resultingImage = process.applyMedianFilter(self.image, size)
        self.updateImage(resultingImage)

    def updateImage(self, newImage, updateHistory=True):
        # Update displayed image
        self.imageThumbnail = access.prepImageForWindow(newImage) # Create thumbnail to be displayed
        self.imageLabel.config(image=self.imageThumbnail)
        self.image = newImage
        print("Image updated.")

        if updateHistory:
            # Update history panel
            self.history.append(self.image.copy())
            self.updateHistoryThumbnails()
            print("History updated.")

        # Update histogram
        self.getHist()
        print("Histogram updated.")

    def toggleOriginalImage(self):
        if self.historyToggle == False:
            self.imagePlaceholder = self.image
            self.historyToggle = True
            self.updateImage(self.history[0], False)
            print("Comparison toggle -> Original")
        else:
            self.updateImage(self.imagePlaceholder, False)
            self.imagePlaceholder = None
            self.historyToggle = False
            print("Comparison toggle -> Recent")
            

if __name__ == "__main__":
    default = Window()
    default.run()
