import cv2,subprocess
from datetime import datetime
import numpy as np
from PIL import Image,ImageFilter
image = cv2.imread('test23.png')

# Boyutlandırma: Oranları koruyarak boyutu iki katına çıkar
height, width = image.shape[:2]
new_size = (width * 4, height * 4)
resized_image = cv2.resize(image, new_size, interpolation=cv2.INTER_LANCZOS4)

# Keskinleştirme (Sharpening) maskesi oluşturma
kernel_sharpening = np.array([[-1, -1, -1],
                              [-1,  9, -1],
                              [-1, -1, -1]])

# Keskinleştirme filtresi uygula
sharpened_image = cv2.filter2D(resized_image, -1, kernel_sharpening)

# Pikselleşmeyi azaltma (Denoising)
denoised_image = cv2.fastNlMeansDenoisingColored(sharpened_image, None, 10, 10, 7, 21)
out = str(datetime.now().strftime("%Y%m%d%H%M%S"))+'output_image.jpg'
# Sonuçları görselleştir
back = cv2.resize(denoised_image,(width,height),interpolation=cv2.INTER_CUBIC)
# Kaydetme (isteğe bağlı)
cv2.imwrite(out, denoised_image)
cv2.imwrite("sm"+out, back)

im = "sm"+out
scale = 4
image = Image.open(im)
sharpened=image.filter(ImageFilter.DETAIL)
sharpened.save("detay_düzetilmis_buyutulmus_resim.png")
smooth = sharpened.filter(ImageFilter.EDGE_ENHANCE)
smooth.save("smooth_düzetilmis_buyutulmus_resim.png")
detail_img = smooth.filter(ImageFilter.SHARPEN)
detail_img.save("sharpen_düzetilmis_buyutulmus_resim.png")
sharp_img = detail_img.filter(ImageFilter.SMOOTH)
sharp_img.save("final_düzetilmis_buyutulmus_resim.png")

image.filter(ImageFilter.EDGE_ENHANCE).save('1akenar_düzeltme.png')
image.filter(ImageFilter.SHARPEN).filter(ImageFilter.SMOOTH).save('1akeskin.png')
image.filter(ImageFilter.SMOOTH).save('1aYumusat.png')
image.filter(ImageFilter.DETAIL).save('1aDetay.png')


# new test
f = 'test23.png'
scale = 2
image = Image.open(f)

width, height = image.size

new_width = width * 2
new_height = height * 2

image.resize((new_width, new_height), Image.LANCZOS).filter(ImageFilter.SHARPEN).resize((width,height), Image.LANCZOS).filter(ImageFilter.SMOOTH).save('demo1.png')
image.resize((new_width, new_height), Image.LANCZOS).filter(ImageFilter.SHARPEN).resize((width,height), Image.LANCZOS).filter(ImageFilter.SMOOTH).filter(ImageFilter.EDGE_ENHANCE).save('demo2.png')

