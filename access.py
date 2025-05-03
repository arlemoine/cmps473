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

def saveImage(image):
    """Save image to specified file path."""
    try:
        # Open a file save dialog to choose where to save image
        filepath = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("All Files", "*.*")],
            title="Save Image As"
        )

        if filepath:
            image.save(filepath)
            print(f"Image saved successfully to {filepath}")
        else:
            print("No file selected. Image not saved.")
    except Exception as e:
        print(f"Error saving image: {e}")

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

    sortedKernelDict = dict(sorted(kernelDict.items()))

    return sortedKernelDict

def normalizeDirName(name):
    """
    Normalize the name of the kernel directory.
    """
    # Normalize the name for filesystem use
    folderName_v1 = name.lower() # Make directory all lower-case
    folderName_v2 = folderName_v1.replace(" ", "_") # Replace spaces in directory name with "_"
    return folderName_v2

def saveKernel(name, matrix):
    folderName = normalizeDirName(name)
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

def saveRecipe(recipeName, tempRecipe):
    """
    Save recipe as json file.
    """
    folderName = normalizeDirName(recipeName)
    folderPath = Path("./recipe") / folderName
    filePath = folderPath / "recipe.json"

    # Make sure the folder path exists
    folderPath.mkdir(parents=True, exist_ok=True)

    # Save the recipe
    recipeData = {
        "name": recipeName,
        "recipe": tempRecipe
    }

    try:
        with open(filePath, "w") as f:
            json.dump(recipeData, f, indent=4)
        print(f"Saved recipe '{recipeName}' to {filePath}")
    except Exception as e:
        print(f"Error saving recipe '{recipeName}': {e}")

def loadRecipe():
    """
    Opens a file dialog to select a recipe JSON file, loads and returns the list of steps.
    
    Returns:
        list[dict] or None
    """
    filepath = filedialog.askopenfilename(
        filetypes=[("JSON Files", "*.json")],
        title="Open Recipe File"
    )

    if not filepath:
        return None

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)

        steps = data.get("recipe")

        if isinstance(steps, list):
            return steps
        else:
            print("Error: Recipe file must contain a list of steps.")
            return None
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading recipe from file: {e}")
        return None
