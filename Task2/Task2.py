import cv2
import os

# Kullanılacak fotoğraf
image = "image.jpg"

# Fotoğrafı oku
img = cv2.imread(image)

# Gri tonlamaya dönüştürme
gri_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Gri filtre uyguladığımız fotoğraf için dizin kopyaladık
dizin = os.path.dirname(os.path.abspath(image))
yeni_dosya = os.path.join(dizin, "image_gri.png")

cv2.imwrite(yeni_dosya, gri_img)

cv2.imshow("Kars Kalesi Normal", img)
cv2.imshow("Kars Kalesi Gri", gri_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(f"Fotoğraf Kaydedilmiştir. {yeni_dosya}")