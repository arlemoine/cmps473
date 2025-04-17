from PIL import Image, ImageTk
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

def prepImageForWindow(image, max_size=(300, 300)):
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

