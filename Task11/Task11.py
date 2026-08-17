
import cv2

img = cv2.imread('image.jpg')

# Dikey çevirme (üst-alt)
dikey = cv2.flip(img, 0)

# Yatay çevirme (sağ-sol / ayna)
yatay = cv2.flip(img, 1)

# Her iki yönde çevirme
her_ikisi = cv2.flip(img, -1)

cv2.imshow('Orijinal', img)
cv2.imshow('Yatay', yatay)
cv2.imshow('Dikey', dikey)
cv2.imshow('Her Ikisi', her_ikisi)
cv2.waitKey(0)
cv2.destroyAllWindows()
