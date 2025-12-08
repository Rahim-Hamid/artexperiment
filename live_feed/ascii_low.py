import cv2
import numpy as np
import ctypes

user32 = ctypes.windll.user32
screen_w = user32.GetSystemMetrics(0)
screen_h = user32.GetSystemMetrics(1)

ASCII_CHARS = "@%#*+=-:. "

def compute_ascii_grid():
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.42

    (char_w, char_h), _ = cv2.getTextSize("A", font, font_scale, 1)
    cols = screen_w // char_w

    while True:
        test_line = "A" * cols
        (w, _), _ = cv2.getTextSize(test_line, font, font_scale, 1)
        if w >= screen_w:
            cols -= 1
            break
        cols += 1

    rows = screen_h // (char_h + 2)
    return cols, rows

def ascii_from_gray(gray, cols, rows, ascii_chars):
    small = cv2.resize(gray, (cols, rows), interpolation=cv2.INTER_AREA)
    shades = len(ascii_chars)

    idx = np.minimum((small.astype(np.int32) * shades) // 256, shades - 1)

    return "\n".join("".join(ascii_chars[i] for i in row) for row in idx)

def ascii_to_image(text):
    img = np.zeros((screen_h, screen_w, 3), dtype=np.uint8)

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.42
    color = (255, 255, 255)

    y = 15
    for line in text.split("\n"):
        cv2.putText(img, line, (0, y), font, font_scale, color, 1, cv2.LINE_AA)
        y += 15

    return img

cv2.namedWindow("ASCII", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("ASCII", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Camera error.")
    exit()

cols, rows = compute_ascii_grid()
print("Using grid:", cols, "cols ×", rows, "rows")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    text = ascii_from_gray(gray, cols, rows, ASCII_CHARS)
    img = ascii_to_image(text)

    cv2.imshow("ASCII", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()