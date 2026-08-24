

import cv2
import numpy as np


def bos_fonksiyon(x):
    pass


def kamera_baslat(index=0):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print("Kameraya erişilemedi.")
        exit()
    return cap


def trackbar_olustur():
    cv2.namedWindow("Ayarlar", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Ayarlar", 400, 300)
    cv2.createTrackbar("H Alt", "Ayarlar", 0, 179, bos_fonksiyon)
    cv2.createTrackbar("S Alt", "Ayarlar", 100, 255, bos_fonksiyon)
    cv2.createTrackbar("V Alt", "Ayarlar", 100, 255, bos_fonksiyon)
    cv2.createTrackbar("H Ust", "Ayarlar", 179, 179, bos_fonksiyon)
    cv2.createTrackbar("S Ust", "Ayarlar", 255, 255, bos_fonksiyon)
    cv2.createTrackbar("V Ust", "Ayarlar", 255, 255, bos_fonksiyon)


def trackbar_degerlerini_oku():
    h_alt = cv2.getTrackbarPos("H Alt", "Ayarlar")
    s_alt = cv2.getTrackbarPos("S Alt", "Ayarlar")
    v_alt = cv2.getTrackbarPos("V Alt", "Ayarlar")
    h_ust = cv2.getTrackbarPos("H Ust", "Ayarlar")
    s_ust = cv2.getTrackbarPos("S Ust", "Ayarlar")
    v_ust = cv2.getTrackbarPos("V Ust", "Ayarlar")

    alt_sinir = np.array([h_alt, s_alt, v_alt])
    ust_sinir = np.array([h_ust, s_ust, v_ust])
    return alt_sinir, ust_sinir


def renk_maskele(frame, alt_sinir, ust_sinir):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, alt_sinir, ust_sinir)

    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    return mask


def nesne_bul_ve_ciz(frame, mask, min_alan=500):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return frame

    largest = max(contours, key=cv2.contourArea)

    if cv2.contourArea(largest) < min_alan:
        return frame

    M = cv2.moments(largest)
    if M["m00"] == 0:
        return frame

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    cv2.circle(frame, (cx, cy), 7, (0, 255, 0), -1)
    x, y, w, h = cv2.boundingRect(largest)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.putText(frame, f"({cx}, {cy})", (cx + 10, cy),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)

    return frame


def temizle(cap):
    cap.release()
    cv2.destroyAllWindows()


def main():
    cap = kamera_baslat()
    trackbar_olustur()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        alt_sinir, ust_sinir = trackbar_degerlerini_oku()
        mask = renk_maskele(frame, alt_sinir, ust_sinir)
        frame = nesne_bul_ve_ciz(frame, mask)

        cv2.imshow("Sonuc", frame)
        cv2.imshow("Maske", mask)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    temizle(cap)


if __name__ == "__main__":
    main()