import cv2
import numpy as np
from PIL import Image
import ctypes
import time


user32 = ctypes.windll.user32
screen_w = user32.GetSystemMetrics(0)
screen_h = user32.GetSystemMetrics(1)

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Camera error.")
    exit()

def block_dither(frame, block_size=10):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape

    small_h = h // block_size
    small_w = w // block_size

    small = cv2.resize(gray, (small_w, small_h), interpolation=cv2.INTER_AREA)

    _, bw = cv2.threshold(small, 128, 255, cv2.THRESH_BINARY)

    block_img = cv2.resize(bw, (screen_w, screen_h), interpolation=cv2.INTER_NEAREST)

    return cv2.cvtColor(block_img, cv2.COLOR_GRAY2BGR)

cv2.namedWindow("BLOCK", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("BLOCK", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    img = block_dither(frame, block_size=12)
    cv2.imshow("BLOCK", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break
