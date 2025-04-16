from PIL import Image, ImageTk

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
