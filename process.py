from PIL import Image
import numpy as np
from scipy.signal import convolve2d # Maybe?
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def applyKernelToImage(pilImage, kernel):
    """Applies a convolution kernel to a grayscale version of the image."""
    grayscale = pilImage.convert("L")
    imageArray = np.array(grayscale, dtype=np.float32)
    kernel = np.array(kernel, dtype=np.float32)
    ksum = kernel.sum()
    if abs(ksum) > 1e-6 and abs(ksum - 1.0) > 1e-6: # Ensures kernel is normalized prior to use
        kernel /= ksum

    # Pad='same' keeps image size consistent
    resultArray = convolve2d(imageArray, kernel, mode="same", boundary="symm")

    # Clip values and convert back to uint8
    resultArray = np.clip(resultArray, 0, 255).astype("uint8")
    return Image.fromarray(resultArray)

def getHistogram(image: Image):
    """
    Takes a PIL Image in grayscale, computes its histogram, and returns the histogram data.
    """
    # Convert image to grayscale if it isn't already
    grayscale_image = image.convert("L")

    # Flatten image pixels to a 1D numpy array
    pixel_data = np.array(grayscale_image).flatten()

    # Generate the histogram data
    hist, bins = np.histogram(pixel_data, bins=256, range=(0, 255))

    # Return the histogram data
    return hist, bins

def generateHistogramPlot(hist, bins):
    """
    Generates and returns a matplotlib figure for the histogram.
    """
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(bins[:-1], hist, width=1, color='black', alpha=0.7)
    ax.set_title("Histogram of Image")
    ax.set_xlabel("Pixel Intensity")
    ax.set_ylabel("Frequency")
    return fig
