from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import urllib.request
from urllib import parse
import time
import os
import uuid
import config
import subprocess
import shutil
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
from PIL import Image
import cv2
import numpy as np
import math
import io

class crawler:
    def __init__(self):
        self.driver = None
        self.open()
        
    def open(self):
        self.download_path = os.path.join(config.DOWNLOAD_TEMP_PATH, str(uuid.uuid4()))
        chrome_driver_path = config.CHROM_DRIVER_PATH

        # download_temp/uuid 폴더 생성
        if not os.path.exists(self.download_path): 
            os.makedirs(self.download_path)
        
        # 크롬 드라이버 설정
        options = Options()
        options.add_argument("headless")  # headless 모드
        options.add_argument("--start-maximized")

        # 창을 뜨지 않게 하는 추가 옵션
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_experimental_option("prefs", {
            "download.default_directory": os.path.join(self.download_path),
        })

        # Specify the ChromeDriver's path using Service
        service = Service(executable_path=chrome_driver_path)

        self.driver = webdriver.Chrome(service=service, options=options)
        self.window_size = self.driver.get_window_size()

    def close(self):
        self.driver.close()
        if os.path.exists(self.download_path):
            shutil.rmtree(self.download_path)

    def create_html(self, htmlbody):
        filepath = self.download_path+'\\'+str(uuid.uuid4())+'.html'
        with open(filepath, "w", encoding="utf-8") as file:
            file.write(htmlbody)
        return filepath
    
    def get(self, url:str):
        self.driver.get(url)
    
    def refresh(self):
        # 페이지 새로고침
        self.driver.refresh()
    
    def maximize_window(self):
        self.driver.maximize_window()
        self.window_size = self.driver.get_window_size()

    def readHTML(self) -> str:
        return self.driver.page_source

    # 페이지가 완전히 로드될 때까지 대기
    def page_loading_wait(self, sec=10) -> bool:
        while sec > 0:
            time.sleep(0.5)  # 5초 대기
            if(
                self.driver.execute_script("return document.readyState") == "complete"
                and self.driver.execute_script("try{return jQuery.active == 0}catch{return true}")
            ): 
                return True
            sec -= 0.5
        return False

    def capture_focus_element(self):
        element = self.driver.switch_to.active_element
        color_img_path, gray_img_path = self.capture_element(element)
        return color_img_path, gray_img_path
    
    def press_tab(self, sec=0.2):
        # ActionChains(self.driver).key_down(Keys.TAB)
        focused_element = self.driver.switch_to.active_element
        focused_element.send_keys(Keys.TAB)
        time.sleep(sec)

    def get_focus_element_body(self) -> str:
        return self.driver.switch_to.active_element.get_attribute('outerHTML')
    
    def is_focus_element_hidden(self) -> bool:
        color_img_path, gray_img_path = self.capture_focus_element()
        if(not color_img_path): return True
        
        # gray_image = cv2.imread(gray_img_path)
        pil_image = Image.open(gray_img_path).convert("RGB")
        opencv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        
        if opencv_image.size and np.all(np.isfinite(opencv_image)):
            std_dev = np.std(opencv_image)
            return std_dev < 3
        return True
        

    def get_focus_element_selector(self) -> str:
        command = """
        function getCssSelector(element) {
            let path = [];
            while (element && element.nodeType === Node.ELEMENT_NODE) {
                let selector = element.nodeName.toLowerCase();

                // 부모에서 동일한 태그 이름을 가진 형제 요소들만 필터링
                if (element.parentNode) {
                    let siblings = Array.from(element.parentNode.children).filter((e) => e.nodeName === element.nodeName);
                    if (siblings.length > 1) {
                        // nth-of-type을 사용하여 정확한 인덱스를 지정
                        let index = Array.prototype.indexOf.call(siblings, element) + 1;
                        selector += `:nth-of-type(${index})`;
                    }
                }
                
                path.unshift(selector);
                element = element.parentNode;
            }
            return path.join(" > ");  // 부모-자식 관계로 셀렉터 생성
        }
        return getCssSelector(document.activeElement);
        """
        return self.driver.execute_script(command)
    
    def tab_until_finish(self, tab_limit=300, tab_cnt_limit=20):
        # 탭 이동 후, item 생성
        tab_selector_dict = {}
        tab_hidden_dict = {}
        
        finish_check = False
        tab_index = -1
        tab_cnt = 0
        tab_end_selector = self.get_focus_element_selector()
        
        while(tab_index < tab_limit):
            self.press_tab()
            tab_item_key = self.get_focus_element_selector()
            
            # 탭 아이템이 끝에 도달한 경우 break
            if(tab_item_key == tab_end_selector): 
                finish_check = True
                break
            
            # 탭 아이템이 중복인 경우 break
            if(tab_item_key in tab_selector_dict): 
                tab_cnt += 1
                if(tab_cnt > tab_cnt_limit):
                    finish_check = False
                    break
                continue
            
            tab_cnt = 0
            tab_index += 1
            # 탭 아이템이 시각적으로 보이지 않고 숨겨진 경우
            if(self.is_focus_element_hidden()):
                tab_hidden_dict[self.get_focus_element_selector()] = tab_index
            
            tab_selector_dict[tab_item_key] = tab_index
        
        return finish_check, tab_selector_dict, tab_hidden_dict
    
    def new_window_check(self):
        windows = self.driver.window_handles
        return len(windows) > 1
    
    def auto_loading_audio_check(self) -> str:
        command = """
        function getCssSelector(element) {
            let path = [];
            while (element && element.nodeType === Node.ELEMENT_NODE) {
                let selector = element.nodeName.toLowerCase();

                // 부모에서 동일한 태그 이름을 가진 형제 요소들만 필터링
                if (element.parentNode) {
                    let siblings = Array.from(element.parentNode.children).filter((e) => e.nodeName === element.nodeName);
                    if (siblings.length > 1) {
                        // nth-of-type을 사용하여 정확한 인덱스를 지정
                        let index = Array.prototype.indexOf.call(siblings, element) + 1;
                        selector += `:nth-of-type(${index})`;
                    }
                }
                
                path.unshift(selector);
                element = element.parentNode;
            }
            return path.join(" > ");  // 부모-자식 관계로 셀렉터 생성
        }
        const mediaElements = [...document.querySelectorAll('audio')];
        const element = mediaElements.find(media => !media.paused);
        if(element) return getCssSelector(element);
        return "";
        """
        result = self.driver.execute_script(command)
        if(result): return result
        
        # 모든 iframe 가져오기
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        # 각 iframe을 순회
        for index, iframe in enumerate(iframes):
            # iframe으로 전환
            self.driver.switch_to.frame(iframe)
            result = self.driver.execute_script(command)
            if(result): return result
            self.driver.switch_to.default_content()
        return ""
    
    def auto_loading_video_check(self) -> str:
        command = """
        function getCssSelector(element) {
            let path = [];
            while (element && element.nodeType === Node.ELEMENT_NODE) {
                let selector = element.nodeName.toLowerCase();

                // 부모에서 동일한 태그 이름을 가진 형제 요소들만 필터링
                if (element.parentNode) {
                    let siblings = Array.from(element.parentNode.children).filter((e) => e.nodeName === element.nodeName);
                    if (siblings.length > 1) {
                        // nth-of-type을 사용하여 정확한 인덱스를 지정
                        let index = Array.prototype.indexOf.call(siblings, element) + 1;
                        selector += `:nth-of-type(${index})`;
                    }
                }
                
                path.unshift(selector);
                element = element.parentNode;
            }
            return path.join(" > ");  // 부모-자식 관계로 셀렉터 생성
        }
        const mediaElements = [...document.querySelectorAll('video')];
        const element = mediaElements.find(media => !media.paused);
        if(element) return getCssSelector(element);
        return "";
        """
        result = self.driver.execute_script(command)
        if(result): return result
        
        # 모든 iframe 가져오기
        iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
        # 각 iframe을 순회
        for index, iframe in enumerate(iframes):
            # iframe으로 전환
            selector = self.get_css_path(iframe)
            self.driver.switch_to.frame(iframe)
            result = self.driver.execute_script(command)
            if(result): return selector
            self.driver.switch_to.default_content()
        return ""
    
    def capture_element(self, element):
        if(element is None 
           or element.size["width"] == 0): 
            return None, None
        capture_img_path = self.download_path+'\\'+str(uuid.uuid4())+'.png'
        # 해당 요소를 캡처하여 이미지로 저장
        element.screenshot(capture_img_path)
        
        # 회색 이미지 저장
        gray_img_path = self.download_path+'\\'+str(uuid.uuid4())+'.png'
        img = Image.open(capture_img_path)
        img_gray = img.convert("L")
        img_gray.save(gray_img_path)
        
        return capture_img_path, gray_img_path
    
    
    def all_img_capture(self):
        img_selector_dict = {}
        
        img_list = self.driver.find_elements(By.TAG_NAME, "img")
        for index, element in enumerate(img_list, start=1):
            color_img_path, gray_img_path = self.capture_element(element)
            if color_img_path:
                selector = self.get_css_path(element)
                img_selector_dict[selector] = {
                    'color_img_path' : color_img_path,
                    'gray_img_path' : gray_img_path
                }
        
        input_list = self.driver.find_elements(By.CSS_SELECTOR, "input[type='image']")
        for index, element in enumerate(input_list, start=1):
            color_img_path, gray_img_path = self.capture_element(element)
            if color_img_path:
                selector = self.get_css_path(element)
                img_selector_dict[selector] = {
                    'color_img_path' : color_img_path,
                    'gray_img_path' : gray_img_path
                }
        
        area_list = self.driver.find_elements(By.TAG_NAME, "area")
        for index, element in enumerate(area_list, start=1):
            color_img_path, gray_img_path = self.capture_element(element)
            if color_img_path:
                selector = self.get_css_path(element)
                img_selector_dict[selector] = {
                    'color_img_path' : color_img_path,
                    'gray_img_path' : gray_img_path
                }
        return img_selector_dict
    
    def all_control_capture(self):
        selector_dict = {}
        
        input_list = self.driver.find_elements(By.CSS_SELECTOR, 'input:not([type="hidden"]):not([type="image"])')
        for index, element in enumerate(input_list, start=1):
            color_img_path, gray_img_path = self.capture_element(element)
            if color_img_path:
                selector = self.get_css_path(element)
                selector_dict[selector] = {
                    'color_img_path' : color_img_path,
                    'gray_img_path' : gray_img_path
                }
        
        button_list = self.driver.find_elements(By.TAG_NAME, "button")
        for index, element in enumerate(button_list, start=1):
            color_img_path, gray_img_path = self.capture_element(element)
            if color_img_path:
                selector = self.get_css_path(element)
                selector_dict[selector] = {
                    'color_img_path' : color_img_path,
                    'gray_img_path' : gray_img_path
                }
        
        textarea_list = self.driver.find_elements(By.TAG_NAME, "textarea")
        for index, element in enumerate(textarea_list, start=1):
            color_img_path, gray_img_path = self.capture_element(element)
            if color_img_path:
                selector = self.get_css_path(element)
                selector_dict[selector] = {
                    'color_img_path' : color_img_path,
                    'gray_img_path' : gray_img_path
                }
        return selector_dict
    
    def all_control_size(self):
        selector_dict = {}
        
        input_list = self.driver.find_elements(By.CSS_SELECTOR, 'input:not([type="hidden"]):not([type="image"])')
        for index, element in enumerate(input_list, start=1):
            size = element.size
            if(size['width'] > 0):
                selector = self.get_css_path(element)
                selector_dict[selector] = {
                    'width' : size["width"],
                    'height' : size["height"],
                    'diagonal' : math.sqrt(size["width"] ** 2 + size["height"] ** 2)
                }
        
        button_list = self.driver.find_elements(By.TAG_NAME, "button")
        for index, element in enumerate(button_list, start=1):
            size = element.size
            if(size['width'] > 0):
                selector = self.get_css_path(element)
                selector_dict[selector] = {
                        'width' : size["width"],
                        'height' : size["height"],
                        'diagonal' : math.sqrt(size["width"] ** 2 + size["height"] ** 2)
                }
        
        textarea_list = self.driver.find_elements(By.TAG_NAME, "textarea")
        for index, element in enumerate(textarea_list, start=1):
            size = element.size
            if(size['width'] > 0):
                selector = self.get_css_path(element)
                selector_dict[selector] = {
                        'width' : size["width"],
                        'height' : size["height"],
                        'diagonal' : math.sqrt(size["width"] ** 2 + size["height"] ** 2)
                }
        return selector_dict
    
    def get_css_path(self, element):
        """Generate CSS path of a Selenium WebElement, counting only previous siblings."""
        path = []
        while element is not None:
            # 태그 이름 가져오기
            tag = element.tag_name
            selector = tag

            if tag == "html":
                path.insert(0, selector)
                break

            # 이전 형제 요소 중 같은 태그 개수 세기
            previous_siblings = element.find_elements(By.XPATH, f"./preceding-sibling::{tag}")
            if previous_siblings:
                index = len(previous_siblings) + 1
                selector += f":nth-of-type({index})"

            path.insert(0, selector)

            # 부모로 이동
            element = element.find_element(By.XPATH, "./..")

        return " > ".join(path)
    
    def capture_full_screenshot(self, gray=True):
        scroll_height = self.driver.execute_script("return document.querySelector(\"html\").scrollHeight")
        self.driver.set_window_size(self.window_size["width"], scroll_height)
        
        capture_img_path = self.download_path+'\\'+str(uuid.uuid4())+'.png'
        
        png = self.driver.get_screenshot_as_png()
        self.maximize_window()

        image = Image.open(io.BytesIO(png))
        if(gray):
            image = image.convert("L")

        # 이미지를 바이트로 다시 변환
        byte_io = io.BytesIO()  # BytesIO 객체 생성
        image.save(byte_io, format="PNG")  # PNG 형식으로 저장
        image_bytes = byte_io.getvalue()  # BytesIO 객체에서 바이트 데이터 추출
        with open(capture_img_path, "wb") as file:
            file.write(image_bytes)

        return capture_img_path