
# Thresholding nedir, hangi alanlarda kullanılır araştırın ve bir yaprak resmi üzerinde bu işlemi gerçekleştirin.

import cv2
import numpy as np

#1. Görüntüyü oku
img = cv2.imread('yaprak.jpg')          # kendi dosya adınla değiştir
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 2. Gürültü azaltmak için hafif blur
blur = cv2.GaussianBlur(gray, (5, 5), 0)

# 3. Otsu ile otomatik eşikleme
# Arkaplan açık (beyaz), yaprak koyu -> INV kullanıyoruz ki yaprak beyaz (255) olsun
otsu_val, thresh = cv2.threshold(
    blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
)
print(f"Otsu'nun bulduğu eşik değeri: {otsu_val}")

# 4. Morphology ile küçük gürültüleri temizle
kernel = np.ones((5, 5), np.uint8)
mask_clean = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)   # küçük delikleri kapat
mask_clean = cv2.morphologyEx(mask_clean, cv2.MORPH_OPEN, kernel)  # küçük gürültü noktalarını sil

# 5. Kontur bul 
contours, _ = cv2.findContours(
    mask_clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
)
largest = max(contours, key=cv2.contourArea) # Burada large contour u bulmamızın sebebi en belirgin tek bir nesneyi ortaya çıkarmak
print(f"Bulunan kontur sayisi: {len(contours)}")
print(f"En büyük konturun alani: {cv2.contourArea(largest):.0f} piksel")

# Konturu orijinal görüntü üzerine kırmızı çizgiyle çiz
result = img.copy()
cv2.drawContours(result, [largest], -1, (0, 0, 255), 3) # ikinci parametre dizi olmalı o nedenle largest [] içine alındı

# 6. Sonucu kaydet
cv2.imwrite('result.jpg', result)

cv2.imshow("Result", result)
cv2.imshow("Normal", img)
cv2.waitKey(0)
cv2.destroyAllWindows()