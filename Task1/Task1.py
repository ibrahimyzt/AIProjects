import cv2
import os

# Açılacak fotoğraf
image = "image.jpg"

# Fotoğrafı oku
img = cv2.imread(image)

# Görüntüyü ekranda göster
cv2.imshow("Kars Kalesi", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Aynı dizine farklı isimle kaydet
dizin = os.path.dirname(os.path.abspath(image))
yeni_dosya = os.path.join(dizin, "image_kopya.png")

cv2.imwrite(yeni_dosya, img)
print(f"Fotoğraf kaydedilmiştir: {yeni_dosya}")