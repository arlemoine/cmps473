from PIL import Image, ImageTk
from pathlib import Path
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
import json

def loadImage(filepath):
    """Load image using PIL."""
    print(f"Loading image from: {filepath}")
    try:
        image = Image.open(filepath)
        return image
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def loadKernel():
    filepath = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])

    if not filepath:
        return None

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        if "matrix" in data:
            kernel = data["matrix"]
            return kernel
        else:
            print("Error: No 'matrix' found in the json file.")
            return None
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading kernel from file: {e}")
        return None

def prepImageForWindow(image, max_size=(1000, 1000)):
    """Resize and convert an image for display in tkinter."""
    if image:
        image = image.copy() # Avoid altering the original
        image.thumbnail(max_size)
        return ImageTk.PhotoImage(image)
    return None

def loadKernelList():
    kernelDict = {}

    # Look for JSON files in all subfolders under ./kernel/
    basePath = Path("./kernel")
    for jsonFile in basePath.glob("*/kernel.json"):  # matches ./kernel/*/something.json
        try:
            with open(jsonFile, "r") as f:
                data = json.load(f)
                name = data.get("name")
                matrix = data.get("matrix")

                if name and matrix:
                    kernelDict[name] = matrix
                else:
                    print(f"Warning: {jsonFile} missing 'name' or 'matrix'")
        except Exception as e:
            print(f"Failed to load {jsonFile}: {e}")

    return kernelDict


def saveKernel(name, matrix):
    # Normalize the name for filesystem use
    folderName = name.lower().replace(" ", "_")
    folderPath = Path("./kernel") / folderName
    filePath = folderPath / "kernel.json"

    # Make sure the folder exists
    folderPath.mkdir(parents=True, exist_ok=True)

    # Save the kernel
    kernelData = {
        "name": name,
        "matrix": matrix
    }

    try:
        with open(filePath, "w") as f:
            json.dump(kernelData, f, indent=4)
        print(f"Saved kernel '{name}' to {filePath}")
    except Exception as e:
        print(f"Error saving kernel '{name}': {e}")
