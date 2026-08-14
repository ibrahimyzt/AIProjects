import cv2

# Kullanılacak fotoğraf
image = "image.jpg"

# Fotoğrafı oku
img = cv2.imread(image)

# Gri tonlamaya dönüştürme
gri_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imwrite("image_gri.png", gri_img)

cv2.imshow("Kars Kalesi Normal", img)
cv2.imshow("Kars Kalesi Gri", gri_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Fotoğraf Kaydedilmiştir.")