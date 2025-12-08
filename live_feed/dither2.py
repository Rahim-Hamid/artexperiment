import cv2
import numpy as np
from PIL import Image
import time
import ctypes

user32 = ctypes.windll.user32
screen_w = user32.GetSystemMetrics(0)
screen_h = user32.GetSystemMetrics(1)

cv2.namedWindow("DITHER", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("DITHER", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

def dither_effect(cv2_frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)
    dithered = pil_img.convert("P", dither=Image.FLOYDSTEINBERG)

    arr = np.array(dithered).astype(np.uint8)
    return arr


cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera Not Open")
    exit()

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame Capture Failed")
            break
        
        dither_frame = dither_effect(frame)
        dither_frame = cv2.resize(dither_frame, (screen_w, screen_h), interpolation=cv2.INTER_LINEAR)
        cv2.imshow("DITHER", dither_frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

        print("Captured & displayed dithered frame. Waiting 30 seconds...")
        time.sleep(30)

finally:
    cap.release()
    cv2.destroyAllWindows()