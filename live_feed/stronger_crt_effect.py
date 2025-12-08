import cv2
import numpy as np
from PIL import Image
import time
import ctypes

user32 = ctypes.windll.user32
screen_w = user32.GetSystemMetrics(0)
screen_h = user32.GetSystemMetrics(1)

cv2.namedWindow("CRT", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("CRT", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)


def add_scanlines(img, intensity=0.4):
    h, w = img.shape[:2]

    line_mask = np.array([
        1 - intensity if y % 2 == 0 else 1
        for y in range(h)
    ], dtype=np.float32)

    line_mask = np.repeat(line_mask[:, np.newaxis], w, axis=1)
    line_mask = line_mask[:, :, np.newaxis]  

    return (img.astype(np.float32) * line_mask).astype(np.uint8)

def add_scanline_wobble(img, intensity=2):
    h, w = img.shape[:2]
    distorted = np.zeros_like(img)

    for y in range(h):
        shift = int(np.sin(y * 0.05 + time.time() * 5) * intensity)
        distorted[y] = np.roll(img[y], shift, axis=0)

    return distorted

def add_rgb_mask(img, strength=0.25):
    h, w = img.shape[:2]
    mask = np.zeros_like(img, dtype=np.float32)

    for x in range(w):
        if x % 3 == 0:
            mask[:, x, 0] = 1.0  
        elif x % 3 == 1:
            mask[:, x, 1] = 1.0  
        else:
            mask[:, x, 2] = 1.0  

    
    out = img.astype(np.float32) * (1 - strength) + mask * 255 * strength
    return np.clip(out, 0, 255).astype(np.uint8)

def add_bloom(img, amount=12):
    blurred = cv2.GaussianBlur(img, (0, 0), amount)
    return cv2.addWeighted(img, 0.6, blurred, 0.4, 0)

def add_curvature(img, strength=0.1):
    h, w = img.shape[:2]

    x, y = np.meshgrid(
        np.linspace(-1, 1, w),
        np.linspace(-1, 1, h)
    )

    r = np.sqrt(x*x + y*y)

    k = strength
    x_distorted = x * (1 + k * (r*r))
    y_distorted = y * (1 + k * (r*r))

    map_x = ((x_distorted + 1) * w) / 2
    map_y = ((y_distorted + 1) * h) / 2

    return cv2.remap(img, map_x.astype(np.float32), map_y.astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)

def add_chromatic_aberration(img, amount=2):
    b, g, r = cv2.split(img)

    b = np.roll(b,  amount, axis=1)
    r = np.roll(r, -amount, axis=1)

    return cv2.merge([b, g, r])

def add_noise(img, intensity=30):
    h, w = img.shape[:2]
    noise = np.random.randint(-intensity, intensity, (h, w, 1), dtype=np.int16)
    noise = np.repeat(noise, 3, axis=2)

    noisy = img.astype(np.int16) + noise
    return np.clip(noisy, 0, 255).astype(np.uint8)

def crt_effect(frame):
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    img = add_bloom(img, amount=8)
    img = add_rgb_mask(img, strength=0.3)
    img = add_scanlines(img, intensity=0.25)
    img = add_curvature(img, strength=0.003)
    img = add_chromatic_aberration(img, amount=5)
    img = add_scanline_wobble(img, intensity=2)
    img = add_noise(img, intensity=20)

    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

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
        
        crt_frame = crt_effect(frame)
        crt_frame = cv2.resize(crt_frame, (screen_w, screen_h), interpolation=cv2.INTER_LINEAR)
        cv2.imshow("CRT", crt_frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

        print("Captured & displayed dithered frame. Waiting 30 seconds...")
        time.sleep(30)

finally:
    cap.release()
    cv2.destroyAllWindows()