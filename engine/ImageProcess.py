import cv2
from PIL import Image, ImageChops
import numpy as np
import cv2
import os
import uuid

def image_matching_check(main_image_path, template_image_path, threshold = 0.8):
    # 이미지 로드
    main_image = cv2.imread(main_image_path)  # 메인 이미지
    template = cv2.imread(template_image_path)  # 서브 이미지

    # 템플릿 매칭
    result = cv2.matchTemplate(main_image, template, cv2.TM_CCOEFF_NORMED)

    # 매칭 결과 분석
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 임계값 설정 (0.8 이상으로 설정)
    threshold = 0.8
    return max_val >= threshold

def check_text_contrast(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
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

def flood_fill(image, x, y, label, labels, jump_distance = 150):
    """
    Flood fill algorithm to label connected components in a binary image.
    """

    jump_distance_half = (int)(jump_distance/2)
    stack = [(x, y)]
    height, width = image.shape
    while stack:
        cx, cy = stack.pop()
        if labels[cy, cx] == 0 and image[cy, cx] == 255:
            labels[cy, cx] = label
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), 
                           (-1, -1), (-1, 1), (1, -1), (1, 1),
                           (-jump_distance_half, -jump_distance_half), (-jump_distance_half, jump_distance_half), 
                           (jump_distance_half, -jump_distance_half), (jump_distance_half, jump_distance_half),
                           (-jump_distance_half, 0), (jump_distance_half, 0), (0, -jump_distance_half), (0, jump_distance_half),
                           (-jump_distance, -jump_distance), (-jump_distance, jump_distance),
                           (jump_distance, -jump_distance), (jump_distance, jump_distance),
                           (-jump_distance, 0), (jump_distance, 0), (0, -jump_distance), (0, jump_distance)]:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < width and 0 <= ny < height:
                    stack.append((nx, ny))

def find_connected_regions(binary_image):
    """
    Find connected regions in a binary image using a flood fill algorithm.
    """
    height, width = binary_image.shape
    labels = np.zeros((height, width), dtype=np.int32)
    label = 1

    for y in range(height):
        for x in range(width):
            if binary_image[y, x] == 255 and labels[y, x] == 0:
                flood_fill(binary_image, x, y, label, labels)
                label += 1

    return labels, label - 1

def find_and_save_differences_with_connected_regions(image1_path, image2_path, output_dir):
    """
    Finds connected differing regions between two images and saves them as separate images.
    
    Parameters:
        image1_path (str): Path to the first image.
        image2_path (str): Path to the second image.
        output_dir (str): Directory to save the output images.
    """
    # Load the two images
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)
    
    height, width = image1.size

    # Ensure images have the same mode and size
    if image1.size != image2.size or image1.mode != image2.mode:
        raise ValueError("Images must have the same dimensions and mode")
    
    # Compute the difference between the two images
    diff = ImageChops.difference(image1, image2)
    print(diff)

    # Convert the difference to a binary image
    diff_np = np.array(diff.convert("L"))  # Convert to grayscale
    _, binary_diff = cv2.threshold(diff_np, 20, 255, cv2.THRESH_BINARY)
    
    # Find connected regions
    labels, num_labels = find_connected_regions(binary_diff)
    
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save each connected region as a separate image
    saved_images = []
    image_padding = 150
    for label in range(1, num_labels + 1):
        mask = (labels == label).astype(np.uint8) * 255
        coords = cv2.findNonZero(mask)
        x, y, w, h = cv2.boundingRect(coords)

        cropped_diff = image1.crop(
            (max(0, x-image_padding), 
             max(0, y-image_padding), 
             min(x + w + image_padding, width), 
             min(y + h + image_padding, height))
        )

        if(w*h > 10000):
            output_path = os.path.join(output_dir, f"{str(uuid.uuid4())}.png")
            cropped_diff.save(output_path)
            saved_images.append(output_path)
    
    return saved_images

def is_text_image(gray_img_path, threshold=10) -> bool:
    gray_image = cv2.imread(gray_img_path, cv2.IMREAD_GRAYSCALE)
    
    # 밝기값 표준편차 계산
    std_dev = np.std(gray_image)
    # print(f"Image Standard Deviation: {std_dev}")
    
    # 텍스트 여부 판별
    return std_dev > threshold