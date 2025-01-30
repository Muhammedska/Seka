import cv2,subprocess
from datetime import datetime
import numpy as np
from PIL import Image,ImageFilter

im = "test23.png"
scale = 2
image = Image.open(im)

width, height = image.size

new_width = width * 2
new_height = height * 2

resized_image = image.resize((new_width, new_height), Image.LANCZOS)
sharpened=resized_image.filter(ImageFilter.DETAIL)

smooth = sharpened.filter(ImageFilter.EDGE_ENHANCE)

detail_img = smooth.filter(ImageFilter.SHARPEN)

sharp_img = detail_img.filter(ImageFilter.SMOOTH)


sharp_img.save("buyutulmus_resim.png")
image = image.filter(ImageFilter.GaussianBlur(radius=1))  # Yarıçapı ayarlayarak bulanıklık miktarını kontrol edebilirsiniz

# Keskinleştirme
image = image.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=0))  # Parametreleri ayarlayarak keskinleştirme miktarını kontrol edebilirsiniz

image.save("duzeltilmis_resim.png")