from PIL import Image, ImageOps, ImageFilter
import numpy as np
from scipy.signal import convolve2d # Maybe?
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os

def applyKernelToImage(pilImage, kernel):
    """Applies a convolution kernel to a given grayscale image."""
    imageArray = np.array(pilImage, dtype=np.float32)
    kernel = np.array(kernel, dtype=np.float32)
    ksum = kernel.sum()
    if abs(ksum) > 1e-6 and abs(ksum - 1.0) > 1e-6: # Ensures kernel is normalized prior to use
        kernel /= ksum

    # Pad='same' keeps image size consistent
    resultArray = convolve2d(imageArray, kernel, mode="same", boundary="symm")

    # Clip values and convert back to uint8
    resultArray = np.clip(resultArray, 0, 255).astype("uint8")
    return Image.fromarray(resultArray)

def grayscale(pilImage):
    grayscale = pilImage.convert("L")
    return grayscale

def saveHistogram(image):
    """
    Takes a PIL Image in grayscale, generates a histogram, and saves it as temp/hist.png.
    Overwrites the file if it already exists.
    """
    # Make sure the 'temp' directory exists
    os.makedirs("temp", exist_ok=True)

    # Convert image to grayscale if it isn't already
    grayscale_image = image.convert("L")

    # Flatten image pixels to a 1D numpy array
    pixel_data = np.array(grayscale_image).flatten()

    # Generate the histogram plot
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.bar(np.arange(256), np.histogram(pixel_data, bins=256, range=(0, 255))[0], width=1, edgecolor="black")
    ax.set_xlim(0, 255)
    ax.set_xlabel("Pixel Intensity")
    ax.set_ylabel("Frequency")
    ax.set_title("Histogram of Pixel Intensities")

    # Save plot to temp/hist.png, overwrite if exists
    hist_path = os.path.join("temp", "hist.png")
    fig.savefig(hist_path, bbox_inches="tight")
    plt.close(fig)

    print(f"Histogram saved to {hist_path}")

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

def applyHistEq(image):
    outputImage = ImageOps.equalize(image)
    return outputImage

def applyMedianFilter(image, neighborSize=3):
    outputImage = image.filter(ImageFilter.MedianFilter(size=neighborSize))
    return outputImage
