import cv2
# Açılacak fotoğraf
image = "image.jpg"

# Fotoğrafı oku
img = cv2.imread(image)

# Görüntüyü ekranda göster
cv2.imshow("Kars Kalesi", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("image_kopya.png", img)
print("Fotoğraf kaydedilmiştir")