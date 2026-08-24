

import cv2

# Kameraya eriş (0 = varsayılan kamera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Kameraya erişilemedi!")
    
while True:
    ret, frame = cap.read()
    
    if not ret:
        print("Görüntü alınamadı!")
        break
    
    frame_ = cv2.flip(frame, 1)
    cv2.imshow('Kamera Goruntusu', frame_)

    # 'q' tuşuna basılınca çık
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
