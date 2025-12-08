import cv2
import numpy as np
from PIL import Image
import ctypes

user32 = ctypes.windll.user32
screen_w = user32.GetSystemMetrics(0)
screen_h = user32.GetSystemMetrics(1)

def ascii_binary(frame, cols, rows):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    small = cv2.resize(gray, (cols, rows), interpolation=cv2.INTER_AREA)
    _, bw = cv2.threshold(small, 128, 255, cv2.THRESH_BINARY)

    text = "\n".join(
        "".join("1" if bw[y, x] == 255 else "0" for x in range(cols))
        for y in range(rows)
    )
    return text

def compute_ascii_grid():
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.42

    (char_w, char_h), _ = cv2.getTextSize("0", font, font_scale, 1)
    cols = screen_w // char_w

    while True:
        test_line = "0" * cols
        (w, _), _ = cv2.getTextSize(test_line, font, font_scale, 1)

        if w > screen_w:
            cols -= 1
            break
        cols += 1

    rows = screen_h // (char_h + 2)

    return cols, rows

def ascii_to_green_image(text):
    img = np.zeros((screen_h, screen_w, 3), dtype=np.uint8)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.42
    color = (0, 255, 0)

    y = 15
    for line in text.split("\n"):
        cv2.putText(img, line, (10, y), font, font_scale, color, 1, cv2.LINE_AA)
        y += 15

    return img

cv2.namedWindow("ASCII", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("ASCII", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera error.")
    exit()

cols, rows = compute_ascii_grid()
print("Using ASCII grid: ", cols, "columns x", rows, "rows")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    text = ascii_binary(frame, cols=cols, rows=rows)
    img = ascii_to_green_image(text)

    cv2.imshow("ASCII", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()