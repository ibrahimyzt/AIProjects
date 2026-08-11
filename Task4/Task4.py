import cv2

# Açılacak fotoğraf
image = "image.jpg"

# Fotoğrafı oku
img = cv2.imread(image)

# İçi dolu dikdörtgen çiz (kalınlık: -1 = dolu)
cv2.rectangle(img, (50, 100), (100, 50), (0, 255, 255), -1)

# Görüntüyü göster
cv2.imshow("Sari Cerceveli Alan", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Kaydet
cv2.imwrite("image_cerceveli.png", img)
print("Fotoğraf kaydedilmiştir")