import cv2

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