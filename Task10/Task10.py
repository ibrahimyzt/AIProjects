

import cv2
import numpy as np

# Orijinal resmi oku
orijinal = cv2.imread('sekil.jpg')

# Morfolojik işlemler genelde binary/gri görüntüler üzerinde yapılır
gri = cv2.cvtColor(orijinal, cv2.COLOR_BGR2GRAY)
_, binary = cv2.threshold(gri, 127, 255, cv2.THRESH_BINARY)

# Kernel (yapılandırma elemanı) tanımla
kernel = np.ones((5, 5), np.uint8)

# --- 1. Erozyon (Erosion) ---
# Nesnenin sınırlarını aşındırır, küçültür
erozyon = cv2.erode(binary, kernel, iterations=1)

# --- 2. Genişleme (Dilation) ---
# Nesnenin sınırlarını genişletir, büyütür
genisleme = cv2.dilate(binary, kernel, iterations=1)

# --- 3. Açma (Opening) ---
# Önce erozyon, sonra genişleme -> küçük gürültüleri (noise) temizler
acma = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)

# Sonuçları göster
cv2.imshow('Orijinal (Binary)', binary)
cv2.imshow('Erozyon', erozyon)
cv2.imshow('Genisleme', genisleme)
cv2.imshow('Acma', acma)

cv2.waitKey(0)
cv2.destroyAllWindows()