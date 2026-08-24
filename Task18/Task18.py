

# 1. YOLOv4 dosyalarının yolları ve girdi resmi
import cv2
import numpy as np

MODEL_CONFIG = "yolov4.cfg"
MODEL_WEIGHTS = "yolov4.weights"
CLASS_FILE = "coco.names"
IMAGE_PATH = "persons.jpg"

# 2. COCO sınıflarını oku
with open(CLASS_FILE, "r", encoding="utf-8") as f:
    classes = [line.strip() for line in f.readlines()]

# 3. YOLOv4 modelini yükle
net = cv2.dnn.readNetFromDarknet(
    MODEL_CONFIG,
    MODEL_WEIGHTS
)

# CPU üzerinde çalıştır
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

# 4. YOLO'nun çıktı katmanlarını bul
layer_names = net.getLayerNames()

output_layers = [
    layer_names[i - 1]
    for i in net.getUnconnectedOutLayers().flatten()
]

# 5. Resmi oku
frame = cv2.imread(IMAGE_PATH)

if frame is None:
    print("Resim okunamadı, dosya yolunu kontrol edin!")
    exit()

height, width = frame.shape[:2]

# 6. Confidence ve NMS eşikleri
CONFIDENCE_THRESHOLD = 0.50
NMS_THRESHOLD = 0.40

# 7. Görüntüyü YOLO formatına dönüştür
blob = cv2.dnn.blobFromImage(
    frame,
    scalefactor=1 / 255.0,
    size=(416, 416),
    swapRB=True,
    crop=False
)

net.setInput(blob)

# 8. Modelden tahminleri al
outputs = net.forward(output_layers)

# 9. Tespit sonuçlarını tutacak listeler
boxes = []
confidences = []
class_ids = []


# 10. YOLO çıktısını incele
for output in outputs:

    for detection in output:

        scores = detection[5:]

        class_id = np.argmax(scores)

        confidence = scores[class_id]


        # 11. Sadece "person" sınıfıyla ilgilen
        if classes[class_id] != "person":
            continue

        # 12. Confidence kontrolü
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


# 13. NMS - aynı kişiye ait tekrar eden kutuları temizle
indexes = cv2.dnn.NMSBoxes(
    boxes,
    confidences,
    CONFIDENCE_THRESHOLD,
    NMS_THRESHOLD
)

# 14. Sonuçları resme çiz
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
            1
        )

        label = f"Person: {confidence:.2f}"

        cv2.putText(
            frame,
            label,
            (x, max(20, y - 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.3,
            (0, 255, 0),
            1
        )

    print(f"Toplam {len(indexes)} kişi tespit edildi.")
else:
    print("Hiç kişi tespit edilemedi.")


# 15. Sonucu göster ve kaydet
cv2.namedWindow("YOLOv4 - Insan Tespiti", cv2.WINDOW_NORMAL)
cv2.resizeWindow("YOLOv4 - Insan Tespiti", 900, 700)
cv2.imshow("YOLOv4 - Insan Tespiti", frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imwrite("sonuc.jpg", frame)