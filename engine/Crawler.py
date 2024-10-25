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
        # options.add_argument("window-size=1920x1080")  # 창 크기 설정
        options.add_argument("--start-maximized")
        # 창을 뜨지 않게 하는 추가 옵션
        # options.add_argument("--no-sandbox")
        # options.add_argument("--disable-dev-shm-usage")
        # options.add_argument("--disable-gpu")
        options.add_experimental_option("prefs", {
            "download.default_directory": os.path.join(self.download_path),
        })

        # Specify the ChromeDriver's path using Service
        service = Service(executable_path=chrome_driver_path)

        self.driver = webdriver.Chrome(service=service, options=options)

    def close(self):
        self.driver.close()
        # if os.path.exists(self.download_path):
        #     shutil.rmtree(self.download_path)

    def get(self, url:str):
        self.driver.get(url)
    
    def refresh(self):
        # 페이지 새로고침
        self.driver.refresh()
    
    def readHTML(self) -> str:
        return self.driver.page_source

    # 페이지가 완전히 로드될 때까지 대기
    def page_loading_wait(self, sec=10) -> bool:
        while sec > 0:
            time.sleep(0.5)  # 5초 대기
            if self.driver.execute_script("return document.readyState") == "complete": return True
            sec -= 0.5
        return False

    def capture_focus_element(self):
        element = self.driver.switch_to.active_element
        capture_img_path = self.download_path+'\\'+str(uuid.uuid4())+'.png'
        # 해당 요소를 캡처하여 이미지로 저장
        element.screenshot(capture_img_path)
        
        # 회색 이미지 저장
        gray_img_path = self.download_path+'\\'+str(uuid.uuid4())+'.png'
        img = Image.open(capture_img_path)
        img_gray = img.convert("L")
        img_gray.save(gray_img_path)

        return capture_img_path, gray_img_path
    
    def press_tab(self, sec=0.3):
        # ActionChains(self.driver).key_down(Keys.TAB)
        focused_element = self.driver.switch_to.active_element
        focused_element.send_keys(Keys.TAB)
        time.sleep(sec)

    def get_focus_element_body(self) -> str:
        return self.driver.switch_to.active_element.get_attribute('outerHTML')
    
    def is_focus_element_hidden(self) -> bool:
        width = self.driver.execute_script("return document.activeElement.getBoundingClientRect().width;")
        if width == 0: 
            return True
        
        color_img_path, gray_img_path = self.capture_focus_element()
        gray_image = cv2.imread(gray_img_path)
        # os.remove(color_img_path)
        # os.remove(gray_img_path)
        
        std_dev = np.std(gray_image)
        print(std_dev)
        return std_dev < 5

    def get_focus_element_selector(self) -> str:
        command = """
        function getCssSelector(element) {
            if (element.id) {
                return `#${element.id}`;  // id가 있는 경우
            } else {
                let path = [];
                while (element && element.nodeType === Node.ELEMENT_NODE) {
                    let selector = element.nodeName.toLowerCase();
                    if (element.parentNode) {
                        let siblings = Array.from(element.parentNode.children).filter((e) => e.nodeName === element.nodeName);
                        if (siblings.length > 1) {
                            selector += `:nth-child(${Array.prototype.indexOf.call(element.parentNode.children, element) + 1})`;
                        }
                    }
                    path.unshift(selector);
                    element = element.parentNode;
                }
                return path.join(" > ");  // 부모-자식 관계로 셀렉터 생성
            }
        }
        return getCssSelector(document.activeElement);
        """
        return self.driver.execute_script(command)
    
    def tab_until_finish(self, tab_limit=300):
        # 탭 이동 후, item 생성
        tab_selector_dict = {}
        tab_hidden_dict = {}
        
        finish_check = False
        tab_index = -1
        tab_end_selector = self.get_focus_element_selector()
        
        while(tab_index < tab_limit):
            self.press_tab()
            tab_item_key = self.get_focus_element_selector()
            print(tab_item_key)
            
            # 탭 아이템이 끝에 도달한 경우 break
            if(tab_item_key == tab_end_selector): 
                finish_check = True
                break
            
            tab_index += 1
            # 탭 아이템이 중복인 경우 break
            if(tab_item_key in tab_selector_dict): 
                finish_check = False
                break
            
            # 탭 아이템이 시각적으로 보이지 않고 숨겨진 경우
            if(self.is_focus_element_hidden()):
                tab_hidden_dict[self.get_focus_element_selector()] = tab_index
            
            tab_selector_dict[tab_item_key] = tab_index
        
        return finish_check, tab_selector_dict, tab_hidden_dict