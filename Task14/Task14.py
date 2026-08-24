

import cv2
import numpy as np

def bos_fonksiyon(x):
    pass

# Trackbar'ları içeren pencereyi oluştur
cv2.namedWindow("Ayarlar")
cv2.createTrackbar("H Alt", "Ayarlar", 0, 179, bos_fonksiyon)
cv2.createTrackbar("S Alt", "Ayarlar", 0, 255, bos_fonksiyon)
cv2.createTrackbar("V Alt", "Ayarlar", 0, 255, bos_fonksiyon)
cv2.createTrackbar("H Ust", "Ayarlar", 179, 179, bos_fonksiyon)
cv2.createTrackbar("S Ust", "Ayarlar", 255, 255, bos_fonksiyon)
cv2.createTrackbar("V Ust", "Ayarlar", 255, 255, bos_fonksiyon)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kameraya erişilemedi.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Trackbar'lardaki o anki değerleri oku
    h_alt = cv2.getTrackbarPos("H Alt", "Ayarlar")
    s_alt = cv2.getTrackbarPos("S Alt", "Ayarlar")
    v_alt = cv2.getTrackbarPos("V Alt", "Ayarlar")
    h_ust = cv2.getTrackbarPos("H Ust", "Ayarlar")
    s_ust = cv2.getTrackbarPos("S Ust", "Ayarlar")
    v_ust = cv2.getTrackbarPos("V Ust", "Ayarlar")

    alt_sinir = np.array([h_alt, s_alt, v_alt])
    ust_sinir = np.array([h_ust, s_ust, v_ust])

    mask = cv2.inRange(hsv, alt_sinir, ust_sinir) # nesne beyaz, arka plan siyah
    result = cv2.bitwise_and(frame, frame, mask=mask) # Nesne renkli, arka plan siyah

    cv2.imshow("Orijinal", frame) # orjinal görüntü
    cv2.imshow("Maske", mask)
    cv2.imshow("Sonuc", result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
