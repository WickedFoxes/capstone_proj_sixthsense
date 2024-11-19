import numpy as np
import cv2


def check_text_contrast(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    # 흑백 변환 후 이진화
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, mask = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 가장 빈도가 높은 색을 선택
    masked_pixels = img[mask == 255]
    colors, counts = np.unique([tuple(pixel) for pixel in masked_pixels], axis=0, return_counts=True)
    color1 = colors[np.argmax(counts)]

    masked_pixels = img[mask == 0]
    colors, counts = np.unique([tuple(pixel) for pixel in masked_pixels], axis=0, return_counts=True)
    color2 = colors[np.argmax(counts)]

    b1, r1, g1 = color1[0] / 255.0, color1[1] / 255.0, color1[2] / 255.0
    b2, r2, g2 = color2[0] / 255.0, color2[1] / 255.0, color2[2] / 255.0

    r1 = r1 / 12.92 if r1 <= 0.03928 else ((r1 + 0.055) / 1.055) ** 2.4
    g1 = g1 / 12.92 if g1 <= 0.03928 else ((g1 + 0.055) / 1.055) ** 2.4
    b1 = b1 / 12.92 if b1 <= 0.03928 else ((b1 + 0.055) / 1.055) ** 2.4

    r2 = r2 / 12.92 if r2 <= 0.03928 else ((r2 + 0.055) / 1.055) ** 2.4
    g2 = g2 / 12.92 if g2 <= 0.03928 else ((g2 + 0.055) / 1.055) ** 2.4
    b2 = b2 / 12.92 if b2 <= 0.03928 else ((b2 + 0.055) / 1.055) ** 2.4

    l1 = 0.2126 * r1 + 0.7152 * g1 + 0.0722 * b1
    l2 = 0.2126 * r2 + 0.7152 * g2 + 0.0722 * b2

    l1, l2 = max(l1, l2), min(l1, l2)

    ratio = (l1 + 0.05) / (l2 + 0.05)

    return ratio