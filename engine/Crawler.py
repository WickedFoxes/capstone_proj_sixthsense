from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
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
        # options.add_argument("headless")  # Uncomment if you want to run Chrome in headless mode
        options.add_experimental_option("prefs", {
            "download.default_directory": os.path.join(self.download_path),
        })

        # Specify the ChromeDriver's path using Service
        service = Service(executable_path=chrome_driver_path)

        self.driver = webdriver.Chrome(service=service, options=options)

    def close(self):
        self.driver.close()
        if os.path.exists(self.download_path):
            shutil.rmtree(self.download_path)

    def get(self, url:str):
        self.driver.get(url)
        
    def readHTML(self) -> str:
        return self.driver.page_source

    def upload_img_and_item(self, filename):
        img_upload_url = config.ITEM_SAVE_SERVER_NAME + config.SERVER_KEY
        
        # Ensure that MultipartEncoder is correctly assigned
        body = MultipartEncoder(
            fields={
                'image': (
                    os.path.basename(filename), 
                    open(filename, 'rb'), 
                    'image/png'
                )  # MIME type should be valid, like 'image/jpeg'
            }
        )
        
        # Set the correct headers for the multipart content
        headers = {'Content-type': body.content_type}
        
        # Perform the POST request
        response = requests.post(img_upload_url, headers=headers, data=body)
        
        return response