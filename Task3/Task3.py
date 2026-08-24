import cv2

# Açılacak fotoğraf
image = "image.jpg"

# Fotoğrafı oku
img = cv2.imread(image)
print("",img.shape)
# --- Yeniden boyutlandırma ---
boyutlandirilmis_img = cv2.resize(img, (400, 300))

# Belirli bir alanı kırpma (crop)
# Format: img[y_baslangic:y_bitis, x_baslangic:x_bitis]
kirpilmis_img = boyutlandirilmis_img[50:250, 100:350]

# Görüntüleri göster
cv2.imshow("Orijinal", img)
cv2.imshow("Yeniden Boyutlandirilmis", boyutlandirilmis_img)
cv2.imshow("Kirpilmis Alan", kirpilmis_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("image_boyutlandirilmis.png", boyutlandirilmis_img)
cv2.imwrite("image_kirpilmis.png", kirpilmis_img)

print("Tüm görüntüler kaydedildi.")