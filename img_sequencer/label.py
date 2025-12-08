import cv2
import os
import random
import numpy as np
import ctypes

cv2.namedWindow("Labeled Sequence", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Labeled Sequence", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

user32 = ctypes.windll.user32
screen_w = user32.GetSystemMetrics(0)
screen_h = user32.GetSystemMetrics(1)

#image_folder = YOUR PATH HERE
word_list = ["Happy", "Dead", "Joy", "Pain", "Unknown", "It's Ok", "Beauty", "Wow", "Art", "Fine", "Watching", "Hate", "Again",
              "Over", "Again", "Dying", "Hope", "Why", "Ignore", "Attack", "Surprise", "Mourn", "Stop", "Please", "Mercy", "Hate", "Cruelty"]
delay = 1000

images = sorted([img for img in os.listdir(image_folder)
                 if img.lower().endswith((".png", ".jpg", ".jpeg"))])

if not images:
    raise ValueError("No images found in folder.")

def resize_with_aspect(image, max_w, max_h):
    h, w = image.shape[:2]
    scale = min(max_w / w, max_h / h)
    
    nw = int(w * scale)
    nh = int(h * scale)

    resized = cv2.resize(image, (nw, nh), interpolation=cv2.INTER_AREA)
    
    canvas = np.zeros((max_h, max_w, 3), dtype=np.uint8)
    
    x_offset = (max_w - nw) // 2
    y_offset = (max_h - nh) // 2
    
    canvas[y_offset:y_offset + nh, x_offset:x_offset + nw] = resized
    
    return canvas

while True:

    random.shuffle(images)

    for img_name in images:
        img_path = os.path.join(image_folder, img_name)
        frame = cv2.imread(img_path)
        frame = resize_with_aspect(frame, screen_w, screen_h)

        if frame is None:
            continue

        chosen_word = random.choice(word_list)

        h, w, _ = frame.shape
        x = random.randint(10, w - 200)
        y = random.randint(30, h - 10)

        font = cv2.FONT_HERSHEY_SIMPLEX
        scale = 3.0
        thickness = 2

        PADDING = 20

        (text_w, text_h), baseline = cv2.getTextSize(chosen_word, font, scale, thickness)

        rect_x1 = x - PADDING
        rect_y1 = y - text_h - PADDING
        rect_x2 = x + text_w + PADDING
        rect_y2 = y + PADDING

        cv2.rectangle(frame, (rect_x1, rect_y1), (rect_x2, rect_y2), (0, 0, 0), -1)
        cv2.putText(frame, chosen_word, (x, y),
                    font, scale, (255, 255, 255), thickness, cv2.LINE_AA)

        cv2.imshow("Labeled Sequence", frame)

        if cv2.waitKey(delay) == 27:
            cv2.destroyAllWindows()
            quit()