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

    if template.shape[0] > main_image.shape[0] or template.shape[1] > main_image.shape[1]:
        return False

    # 템플릿 매칭
    result = cv2.matchTemplate(main_image, template, cv2.TM_CCOEFF_NORMED)

    # 매칭 결과 분석
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    return max_val >= threshold

def check_text_contrast(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_COLOR)
    return image_contrast(img)

def image_contrast(img):
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
    # print(diff)

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

# 구별이 어려운 부분을 잘라 저장
def check_content_separation(img_path):
    save_dir = os.path.dirname(img_path)
    # 이미지 로드
    image = cv2.imread(img_path)

    height = image.shape[0]
    width = image.shape[1]
    offset = 20

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 에지 검출
    edges = cv2.Canny(gray, 30, 100)

    # 팽창 연산
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (30, 30))
    dilated = cv2.dilate(edges, kernel)

    # 윤곽선 추출
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    objs = []
    ret = []

    for contour in contours:
        if cv2.contourArea(contour) < 1000:  # 작은 영역 제거
            continue
        x, y, w, h = cv2.boundingRect(contour)
        cropped = image[max(y-offset,0):min(y + h + offset, height),max(x-offset,0):min(x + w + offset, width)]
        if(has_divide_line(cropped)): # 구분선이 존재하면 통과
            continue
        objs.append({'xmin':x,'ymin':y,'xmax':x+w,'ymax':y+h,'contrast':image_contrast(cropped)})
    
    root = [i for i in range(len(objs))]
    for i in range(len(objs)):
        rt = i
        while(root[rt] != rt):
            rt = root[rt]
        root[i] = rt
        m = 0
        for j in range(i+1, len(objs)):
            # 가까운 위치에 있고 명도대비가 비슷하면 오류로 처리
            x1, y1, x2, y2, c1 = objs[i]['xmin'],objs[i]['ymin'],objs[i]['xmax'],objs[i]['ymax'], objs[i]['contrast']
            x3, y3, x4, y4, c2 = objs[j]['xmin'],objs[j]['ymin'],objs[j]['xmax'],objs[j]['ymax'], objs[j]['contrast']

            l1, l2 = x4 - x1, x2 - x3
            l3, l4 = y4 - y1, y2 - y3
            l5, l6 = max(-l1, -l2), max(-l3, -l4)

            vertical = l1 > 0 and l2 > 0 and min(l1, l2)/min(x2-x1,x4-x3) > 0.8 and l6 > 0 and l6 < 10
            horizontal = l3 > 0 and l4 > 0 and min(l3, l4)/min(y2-y1,y4-y3) > 0.8 and l5 > 0 and l5 < 10

            # 구별하기 어려운 요소들을 병합
            if (vertical or horizontal) and abs(c1 - c2) < 0.3:
                cur = j
                while(root[cur] != cur):
                    cur = root[cur]
                root[j] = rt
                if cur == rt: continue
                root[cur] = rt
                objs[rt]['xmin'] = min(objs[cur]['xmin'], objs[rt]['xmin'])
                objs[rt]['ymin'] = min(objs[cur]['ymin'], objs[rt]['ymin'])
                objs[rt]['xmax'] = max(objs[cur]['xmax'], objs[rt]['xmax'])
                objs[rt]['ymax'] = max(objs[cur]['ymax'], objs[rt]['ymax'])
                m+=1
        if(rt == i and m == 0):
            root[i] = -1
            
    # 이미지 저장
    for i in range(len(objs)):
        if(i == root[i]):
            xmin, ymin, xmax, ymax = objs[i]['xmin'], objs[i]['ymin'], objs[i]['xmax'], objs[i]['ymax']
            cropped = image[ymin:ymax, xmin:xmax]
            save_path = save_dir + '\\' + str(uuid.uuid4()) + '.png'
            cv2.imwrite(save_path, cropped)
            ret.append(save_path)

    return ret

# 구분선이 존재하는지 판별
def has_divide_line(image) -> bool:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # 흑백 변환

    # 엣지 감지
    edges = cv2.Canny(gray, 5, 20)

    # 모폴로지 연산으로 수평/수직선 강조
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 1))  # 수평선 강조
    horizontal_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 50))  # 수직선 강조
    vertical_lines = cv2.morphologyEx(edges, cv2.MORPH_OPEN, kernel)

    # 전체 구분선 결합
    lines = cv2.add(horizontal_lines, vertical_lines)

    # 허프 변환으로 선 검출
    lines_detected = cv2.HoughLinesP(lines, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=10)
    
    return lines_detected is not None