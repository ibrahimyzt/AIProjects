


# 1. YOLOv4 dosyalarının yolları
import cv2
import numpy as np
import time  # FPS hesaplamak için eklendi

MODEL_CONFIG = "yolov4.cfg"
MODEL_WEIGHTS = "yolov4.weights"
CLASS_FILE = "coco.names"

# 2. COCO sınıflarını oku
with open(CLASS_FILE, "r", encoding="utf-8") as f:
    classes = [line.strip() for line in f.readlines()]

# 3. YOLOv4 modelini yükle
net = cv2.dnn.readNetFromDarknet(
    MODEL_CONFIG,
    MODEL_WEIGHTS
)

# CPU da çalıştır
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# 4. YOLO'nun çıktı katmanlarını bul
layer_names = net.getLayerNames()

output_layers = [
    layer_names[i - 1]
    for i in net.getUnconnectedOutLayers().flatten()
]

# 5. Webcam'i aç
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Webcam açılamadı!")
    exit()

# 6. Confidence ve NMS eşikleri
CONFIDENCE_THRESHOLD = 0.50
NMS_THRESHOLD = 0.40

# 6.1 FPS hesaplaması için başlangıç zamanı
prev_time = time.time()

# 7. Webcam döngüsü
while True:

    ret, frame = cap.read()

    if not ret:
        print("Webcam görüntüsü alınamadı!")
        break

    height, width = frame.shape[:2]

    # 8. Görüntüyü YOLO formatına dönüştür
    blob = cv2.dnn.blobFromImage(
        frame,
        scalefactor=1 / 255.0,
        size=(416, 416),
        swapRB=True,
        crop=False
    )

    net.setInput(blob)

    # 9. Modelden tahminleri al
    outputs = net.forward(output_layers)

    # 10. Tespit sonuçlarını tutacak listeler
    boxes = []
    confidences = []
    class_ids = []

    # 11. YOLO çıktısını incele
    for output in outputs:

        for detection in output:

            scores = detection[5:]

            class_id = np.argmax(scores)

            confidence = scores[class_id]


            # 12. Sadece "person" sınıfıyla ilgilen
            if classes[class_id] != "person":
                continue

            # 13. Confidence kontrolü
            if confidence < CONFIDENCE_THRESHOLD:
                continue


            center_x = int(detection[0] * width)
            center_y = int(detection[1] * height)

            box_width = int(detection[2] * width)
            box_height = int(detection[3] * height)


            x = int(center_x - box_width / 2)
            y = int(center_y - box_height / 2)


            boxes.append([x, y, box_width, box_height])
            confidences.append(float(confidence))
            class_ids.append(class_id)


    # 14. NMS - aynı kişiye ait tekrar eden kutuları temizle
    indexes = cv2.dnn.NMSBoxes(
        boxes,
        confidences,
        CONFIDENCE_THRESHOLD,
        NMS_THRESHOLD
    )

    # 15. Sonuçları ekrana çiz
    if len(indexes) > 0:

        for i in indexes.flatten():

            x, y, w, h = boxes[i]

            confidence = confidences[i]


            x = max(0, x)
            y = max(0, y)

            w = min(w, width - x)
            h = min(h, height - y)

            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

            label = f"Person: {confidence:.2f}"

            cv2.putText(
                frame,
                label,
                (x, max(20, y - 10)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    # 15.1 FPS hesapla ve sağ üst köşeye yazdır
    current_time = time.time()
    fps = 1 / (current_time - prev_time)
    prev_time = current_time

    fps_text = f"FPS: {fps:.1f}"

    # Metnin piksel genişliğini/yüksekliğini ölç, sağa dayamak için kullan
    (text_width, text_height), _ = cv2.getTextSize(
        fps_text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
    )

    margin = 10
    text_x = width - text_width - margin   # sağdan margin kadar içeride başlasın
    text_y = text_height + margin          # üstten margin kadar aşağıda

    cv2.putText(
        frame,
        fps_text,
        (text_x, text_y),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 255),  # sarı, diğer etiketlerden ayırt edilsin diye
        2
    )

    # 16. Görüntüyü göster
    cv2.imshow("YOLOv4 - Insan Tespiti", frame)

    # 17. Q tuşuna basılırsa programı kapat
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 18. Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()