
# Kare içine alınan bu alanı önce griye dönüştürün, ardından bu alanı bulanıklaştırın. 
# Bu işlemlerin gerçek hayatta nerelerde kullanıldığını araştırın.

import cv2


img = cv2.imread("image.jpg")

# Kırpma işlemi / variable = img[ y1:y2, x1:x2] )
kare_alan = img[50:200, 50:200]

# Griye dönüştürme
gri_foto = cv2.cvtColor(kare_alan, cv2.COLOR_BGR2GRAY)

# Bulanıklaştırma
bulanik_foto = cv2.GaussianBlur(gri_foto, (15,15), 0)

# Gri görüntü tek kanallı olduğu için 3 kanala çevirme - orjinal fotoya geri koymak için
bulanik_foto_bgr = cv2.cvtColor(bulanik_foto, cv2.COLOR_GRAY2BGR)

# İşlenmiş bölgeyi orjinal fotoya geri koymak
img[50:200, 50:200] = bulanik_foto_bgr

cv2.imshow("Belirli alani Bulaniklastirilmis Fotograf", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("Belirli_alani_bulaniklastirilmis_fotograf.png", img)
