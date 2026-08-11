import cv2

# Açılacak fotoğraf
image = "image.jpg"

# Fotoğrafı oku
img = cv2.imread(image)

# Dikdörtgenin koordinatları (kendi resmine göre ayarlayabilirsin)
x1, y1 = 50, 100   # sol üst köşe
x2, y2 = 100, 50   # sağ alt köşe

# Sarı renk (OpenCV'de BGR formatında: Blue, Green, Red)
sari_renk = (0, 255, 255)

# İçi dolu dikdörtgen çiz (kalınlık: -1 = dolu)
cv2.rectangle(img, (x1, y1), (x2, y2), sari_renk, -1)

# Görüntüyü göster
cv2.imshow("Sari Cerceveli Alan", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Kaydet
cv2.imwrite("image_cerceveli.png", img)
print("Fotoğraf kaydedilmiştir")