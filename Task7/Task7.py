

import cv2
import numpy as np

# Görüntüyü oku ve gri tona çevir
img = cv2.imread("coins.jpg")
img_cp = cv2.imread("coins.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Otsu eşikleme ile nesne/arka plan ayrımı
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Gürültüyü temizle
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

# Kesin arka plan ve kesin nesne bölgelerini bul
sure_bg = cv2.dilate(opening, kernel, iterations=3)
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
_, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
sure_fg = np.uint8(sure_fg)

# Belirsiz bölgeyi hesapla
unknown = cv2.subtract(sure_bg, sure_fg)

# Marker haritasını oluştur
_, markers = cv2.connectedComponents(sure_fg)
markers = markers + 1
markers[unknown == 255] = 0

# Watershed'i çalıştır ve sınırları kırmızı boya
markers = cv2.watershed(img, markers)
img[markers == -1] = [0, 0, 255]

cv2.imwrite("sonuc.jpg", img)

cv2.imshow("Normal", img_cp)
cv2.imshow("Sonuc", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
