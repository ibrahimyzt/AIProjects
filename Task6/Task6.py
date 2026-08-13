
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

# Sonucu kaydet
cv2.imwrite('result.jpg', thresh)

cv2.imshow("Result", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()