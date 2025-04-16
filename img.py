from PIL import Image
from PIL import ImageFilter

im = Image.open("img/cat.jpg")
im_grayscale = im.convert("L")

kernel_values = (
        .33, .67, .33,
        .67, 1,.67,
        .33, .67, .33
)
kernel_size = (3, 3)

kernel_edge_det = ImageFilter.Kernel(kernel_size, kernel_values, scale=0, offset=0)

im_edge = im_grayscale.filter(kernel_edge_det)
im_edge.show()

