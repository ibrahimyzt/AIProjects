

import cv2
import numpy as np

# 1. YOLOv3 Face modelini yükle

net = cv2.dnn.readNetFromDarknet(    
    # cv2.dnn --> OpenCV 'nin eğitilmiş derin öğrenme modellerini çalıştırmak için sunduğu bir modül.
    #readNetFromDarknet --> YOLO 'nun orijinal geliştirildiği "Darknet" framework'ünün dosya formatını okuyabilen özel bir fonksiyon.

    "yolov3-face.cfg",               # .cfg -> modelin yapılandırma dosyası
    "yolov3-wider_16000.weights"     # .weights -> modelin eğitilmiş ağırlıkları  
)

# YOLO modelinin çıkış katmanlarının isimlerini al
cikis_katmanlari = net.getUnconnectedOutLayersNames()

# 2. Bilgisayarın kamerasını aç
cap = cv2.VideoCapture(0)

# 3. Kamera görüntüsünü sürekli oku
while True:

    # Kameradan bir görüntü al
    ret, frame = cap.read()

    # Görüntü alınamadıysa döngüyü sonlandır
    if not ret:
        break

    # 4. Görüntünün genişlik ve yüksekliğini al
    height, width = frame.shape[:2]

    # 5. Görüntüyü YOLO'nun anlayabileceği formata dönüştür
    blob = cv2.dnn.blobFromImage(
        frame,
        1 / 255.0,              # Piksel değerlerini 0-1 arasına getir
        (416, 416),             # YOLO giriş boyutu
        (0, 0, 0),              # Ortalama çıkarma
        swapRB=True,            # BGR -> RGB
        crop=False
    )
    frame = cv2.flip(frame, 1)


    # Hazırlanan görüntüyü modele gönder
    net.setInput(blob)

    # 6. YOLO'dan sonuçları al
    sonuclar = net.forward(cikis_katmanlari)

    # Tespit edilen yüzlerin kutularını tutacak liste
    kutular = []

    # Her yüzün güven değerini tutacak liste
    guven_skorlari = []

    # 7. YOLO sonuçlarını tek tek incele
    for cikti in sonuclar:

        for tespit in cikti:

            # Modelin yüz için verdiği güven değerini al
            skor = tespit[5]

            # Güven değeri %50'den yüksekse yüz olarak kabul et
            if skor > 0.5:

                # Yüzün merkez noktası ve genişlik/yüksekliğini
                # gerçek görüntü boyutlarına dönüştür
                cx, cy, w, h = (
                    tespit[0:4]
                    * np.array([width, height, width, height])
                ).astype(int)


                # Yüzün sol üst köşesini hesapla
                x = int(cx - w / 2)
                y = int(cy - h / 2)


                # Yüz kutusunu listeye ekle
                kutular.append([
                    x,
                    y,
                    int(w),
                    int(h)
                ])

                # Güven değerini listeye ekle
                guven_skorlari.append(float(skor))


    # 8. Aynı yüz için birden fazla kutu oluşmasını engelle

    indeksler = cv2.dnn.NMSBoxes(
        kutular,
        guven_skorlari,
        0.5,    # Confidence threshold
        0.4     # NMS threshold
    )

    
    # Eğer en az bir yüz tespit edildiyse
    if len(indeksler) > 0:

        # Tespit edilen yüzleri tek tek işle
        for i in indeksler.flatten():

            # Yüz kutusunun koordinatlarını al
            x, y, w, h = kutular[i]

            # Güven değerini yüzdeye çevir
            guven_yuzde = guven_skorlari[i] * 100

            # 9. Yüzün etrafına yeşil kutu çiz
        
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            # 10. Güven değerini yazıya dönüştür
            etiket = f"Yuz: {guven_yuzde:.1f}%"
            
            # 11. Güven değerini yüz kutusunun üzerine yaz
            cv2.putText(
                frame,
                etiket,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )
    # 12. Kameradaki görüntüyü ekranda göster
    cv2.imshow(
        "Canli Yuz Tespiti",
        frame
    )

    # 13. Q tuşuna basılırsa programdan çık
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 14. Kamera ve OpenCV penceresini kapat
cap.release()
cv2.destroyAllWindows()