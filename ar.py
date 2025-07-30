import cv2
import numpy as np

arrow_img = cv2.imread("righty.png")

# Beyaz arka planı kaldır ve alfa kanalı ekle
gray = cv2.cvtColor(arrow_img, cv2.COLOR_BGR2GRAY)
_, alpha = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)

b, g, r = cv2.split(arrow_img)
rgba = [b, g, r, alpha]
arrow_transparent = cv2.merge(rgba, 4)

# Test için kaydedelim:
cv2.imwrite("right.png", arrow_transparent)
