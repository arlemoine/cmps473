from PIL import Image
import numpy as np
from scipy.signal import convolve2d # Maybe?

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
