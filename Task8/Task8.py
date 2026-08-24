

import cv2
import numpy as np

# Görüntüyü oku ve gri tona çevir
img = cv2.imread("cheesboard.jpg")
img_cp = img.copy()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# HARRIS CORNER DETECTION
gray_float = np.float32(gray)
corners = cv2.cornerHarris(gray_float, blockSize=2, ksize=3, k=0.04)

# Köşeleri belirginleştirmek için genişlet
corners = cv2.dilate(corners, None)

# Orijinal görüntü üzerinde köşeleri kırmızı nokta ile işaretle
img_corners = img.copy()
img_corners[corners > 0.01 * corners.max()] = [0, 255, 0]

cv2.imwrite("corners.jpg", img_corners)

# CANNY EDGE DETECTION--
edges = cv2.Canny(gray, threshold1=100, threshold2=200)

cv2.imwrite("edges.jpg", edges)
cv2.imshow("Corners",img_corners)
cv2.imshow("Edges", edges)
cv2.imshow("Normal", img_cp)
cv2.waitKey(0)
cv2.destroyAllWindows()