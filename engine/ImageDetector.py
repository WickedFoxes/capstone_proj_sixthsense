from ultralytics import YOLO
import cv2
import os
import uuid

class image_detector:
    def __init__(self):
        current_dir = os.path.dirname(__file__)
        model_path = os.path.join(current_dir, "model", "yolo832.pt")
        # if(use_640):
        #     model_path = os.path.join(model_path, "yolo640.pt")
        #     self.imgsz = 640
        # else:
        #     model_path = os.path.join(model_path, "yolo1024.pt")
        #     self.imgsz = 1024
        self.model = YOLO(model_path)

    # [{'img_path', 'class_name'}, ...] 배열을 리턴
    def predict(self, img_path, threshold = 0.5):
        results = self.model.predict(source=img_path)
        image = cv2.imread(img_path)
        save_path = os.path.dirname(img_path) # 원본 이미지와 같은 경로에 저장
        ret = []
        for result in results:
            num_class = len(result.names)
            boxes = [box for box in result.boxes if box.conf[0] > threshold] # 신뢰도가 threshold 이상인 것만 사용
            for i in range(num_class):
                boxes_class = [[x for x in box.xyxy[0]] for box in boxes if int(box.cls[0]) == i]
                if len(boxes_class) > 0:
                    ret.extend(self._save_objects(image, boxes_class, result.names[i], save_path))
        return ret
    
    # 두 영역이 겹치는지 판단
    def _is_overlap(self, box1, box2):
        x1, y1, x2, y2 = map(int, box1)
        x3, y3, x4, y4 = map(int, box2)

        if x1 > x4 or x2 < x3:
            return False 
        if y1 > y4 or y2 < y3:
            return False  

        return True

    # 이미지를 잘라서 저장, dictionary 구조로 리턴
    def _save_cropped_img(self, image, area, class_name, path):
        x1, y1, x2, y2 = map(int, area)
        cropped = image[y1:y2, x1:x2]
        save_path = path + '\\' + str(uuid.uuid4()) + '.png'
        cv2.imwrite(save_path, cropped)
        obj = {"img_path": save_path,
            "class_name": class_name}
        return obj
    
    # 겹치는 영역들을 병합하여 저장
    def _save_objects(self, image, array, class_name, save_path):
        ret = []
        while len(array) > 0:
            elem = array[0]
            index = next((i for i, x in enumerate(array) if self._is_overlap(x, elem) and i > 0), None)
            while index is not None: # 더 이상 병합할 수 있는 영역이 없을 때까지 반복
                elem[0] = min(array[index][0], elem[0])
                elem[1] = min(array[index][1], elem[1])
                elem[2] = max(array[index][2], elem[2])
                elem[3] = max(array[index][3], elem[3])
                del array[index]
                index = next((i for i, x in enumerate(array) if self._is_overlap(x, elem) and i > 0), None)
            ret.append(self._save_cropped_img(image, elem, class_name, save_path))
            del array[0]
        return ret