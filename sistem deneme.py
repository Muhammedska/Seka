from PIL import Image, ImageFilter
image = Image.open("test23.png") # "resim.jpg" yerine kendi resminizin adını yazın.
width, height = image.size
new_size = (width*2, height*2) # Boyutları 2 katına çıkarıyoruz.
image = image.resize(new_size, Image.LANCZOS) # LANCZOS en iyi yeniden örnekleme algoritmalarından biridir.
image = image.filter(ImageFilter.GaussianBlur(radius=2)) # Bulanıklık yarıçapını ayarlayabilirsiniz.
image = image.filter(ImageFilter.UnsharpMask(radius=3, percent=150, threshold=0)) # Parametreleri ayarlayarak keskinleştirme miktarını kontrol edebilirsiniz.
image = image.filter(ImageFilter.SMOOTH)
image.save("yenimodel.png")
from PIL import Image, ImageEnhance

image = Image.open("test23.png")

if image.mode != "RGB":
    image = image.convert("RGB")
# Tüm kanallara aynı anda kontrast uygulama
enhancer = ImageEnhance.Contrast(image)
image = enhancer.enhance(1.5)

# Her bir kanala ayrı ayrı kontrast uygulama (daha fazla kontrol sağlar)
r, g, b = image.split()

enhancer_r = ImageEnhance.Contrast(r)
r = enhancer_r.enhance(1.2)

enhancer_g = ImageEnhance.Contrast(g)
g = enhancer_g.enhance(1.2)

enhancer_b = ImageEnhance.Contrast(b)
b = enhancer_b.enhance(1.2)

image = Image.merge("RGB", (r, g, b))
image.save('model2.png')