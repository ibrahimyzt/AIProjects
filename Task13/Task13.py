

import cv2
import numpy as np

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kameraya erişilemedi.")
    exit()

kernel = np.ones((5, 5), np.uint8)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 1. Griye çevir, siyah nesneler için eşikle
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY_INV)

    # 2. Gürültüyü temizle
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    # 3. Kontur bul
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        largest = max(contours, key=cv2.contourArea)

        # çok küçük konturları (gürültü artıkları) görmezden gel
        if cv2.contourArea(largest) > 500:
            M = cv2.moments(largest) # Moment

            if M["m00"] != 0: # M["m00"] : konturun alanı
                cx = int(M["m10"] / M["m00"]) # Centroid x, M["m10"] : x kordinatlarının alan ağırlıklı toplamı
                cy = int(M["m01"] / M["m00"]) # Centroid Y, M["m01"] : y kordinatlarının alan ağırlıklı toplamı

                # merkez noktası
                cv2.circle(frame, (cx, cy), 7, (0, 255, 0), -1)

                # çevresine kutu
                x, y, w, h = cv2.boundingRect(largest)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imshow("Kamera", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()