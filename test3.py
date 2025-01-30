import cv2

image = cv2.imread("test23.png")
height, width = image.shape[:2]
new_size = (width * 2, height * 2)

# En yakın komşu interpolasyonu
resized_image_nearest = cv2.resize(image, new_size, interpolation=cv2.INTER_NEAREST)

# Doğrusal interpolasyon
resized_image_linear = cv2.resize(image, new_size, interpolation=cv2.INTER_LINEAR)

# Bikübik interpolasyon
resized_image_cubic = cv2.resize(image, new_size, interpolation=cv2.INTER_CUBIC)

# Lanczos interpolasyonu
resized_image_lanczos = cv2.resize(image, new_size, interpolation=cv2.INTER_LANCZOS4)

cv2.imshow("Nearest", resized_image_nearest)
cv2.imshow("Linear", resized_image_linear)
cv2.imshow("Cubic", resized_image_cubic)
cv2.imshow("Lanczos", resized_image_lanczos)
cv2.waitKey(0)
cv2.destroyAllWindows()


# ----------------------------------


"""
# Süper çözünürlük modeli yükleme
sr = cv2.dnn_superres.DnnSuperResImpl_create()
sr.readModel("EDSR_x4.pb")  # Model dosyasını indirmen gerekebilir
sr.setModel("edsr", 2)  # EDSR modelini 4x büyütme ile kullan

# Görüntüyü oku ve büyüt
image = cv2.imread("test.png")
result = sr.upsample(image)

# Kaydet
cv2.imwrite("high_res_imagex2.png", result)"""

command = [
    "./AI/waifu2x-ncnn-vulkan.exe",  # Eğer Windows kullanıyorsan: "waifu2x-ncnn-vulkan.exe"
    "-i", "./test23.png",  # Girdi dosyası
    "-o", "./" + str(datetime.now().strftime("%Y%m%d%H%M%S")) + "waifud_31.jpg",  # Çıktı dosyası
    "-s", str(2),  # Büyütme oranı
    "-n", str(3)  # Gürültü azaltma seviyesi
]
subprocess.run(command)
image_path = "test23.png"
output_path = str(datetime.now().strftime("%Y%m%d%H%M%S")) + ".jpg"
scale = 2
image = cv2.imread(image_path)

# Orijinal boyutları al
height, width = image.shape[:2]

# Yeni boyutları hesapla (Oranı koruyarak 2 kat büyüt)
new_width = int(width * scale)
new_height = int(height * scale)

# Görüntüyü yeniden boyutlandır (Bilinear Interpolation)
upscaled = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

# Keskinleştirme filtresi (Unsharp Masking)
blurred = cv2.GaussianBlur(upscaled, (5, 5), 0)
sharpened = cv2.addWeighted(upscaled, 1.5, blurred, -0.5, 0)

# Sonucu kaydet
cv2.imwrite(output_path, sharpened)
# Süper çözünürlük modeli yükleme
sr = cv2.dnn_superres.DnnSuperResImpl_create()
sr.readModel("EDSR_x4.pb")  # Model dosyasını indirmen gerekebilir
sr.setModel("edsr", 2)  # EDSR modelini 4x büyütme ile kullan

# Görüntüyü oku ve büyüt
image = cv2.imread(output_path)
result = sr.upsample(image)

# Kaydet
cv2.imwrite(output_path + "high_res_imagex2.png", result)
# Görüntüyü göster
img = cv2.imread(output_path + "high_res_imagex2.png")

# Pencere oluştur ve resmi göster

cv2.imshow("Upscaled & Sharpened", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
