import config

import os
import json
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder

def get_ready_status_page():
    ready_page_url = config.READ_READY_PAGE_SERVER_NAME + config.SERVER_KEY
    return get_json_data(ready_page_url)

def put_running_status(page_id : int):
    page_status_update_url = config.UPDATE_PAGE_STATUS_SERVER_NAME + config.SERVER_KEY
    return put_json_data(
        page_status_update_url,
        {"id" : page_id, "status": "RUNNING"}
    )

def put_complete_status(page_id : int):
    page_status_update_url = config.UPDATE_PAGE_STATUS_SERVER_NAME + config.SERVER_KEY
    return put_json_data(
        page_status_update_url,
        {"id" : page_id, "status": "COMPLETE"}
    )
    
def delete_page_scanlist(page_id : int):
    page_scanlist_delete_url = config.DELETE_SCANLIST_SERVER_NAME + str(page_id) + "/" + config.SERVER_KEY
    print(page_scanlist_delete_url)
    return delete_json_data(
        page_scanlist_delete_url
    )

def post_create_item(page_id : int, item):
    item_create_url = config.CREATE_ITEM_SERVER_NAME + str(page_id) + "/" + config.SERVER_KEY
    return post_json_data(item_create_url, item)

def post_create_scan(page_id: int, item_id: int, scan):
    scan_create_url = config.CREATE_SCAN_SERVER_NAME + str(page_id) + "/" + str(item_id) +"/" + config.SERVER_KEY
    return post_json_data(scan_create_url, scan)

def post_upload_img(self, img_upload_url, filename):
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

def get_json_data(api_url):
    try:
        # API로 GET 요청 보내기
        response = requests.get(api_url)
        
        # 응답 상태 코드가 200 (성공)일 때만 처리
        if response.status_code == 200:
            # 응답 데이터를 JSON 형식으로 파싱
            json_data = response.json()
            return json_data
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # 예외 처리 (네트워크 오류 등)
        print(f"An error occurred: {e}")
        return None

def post_json_data(api_url, data):
    headers = {
        'Content-Type': 'application/json'  # JSON 데이터를 보낼 때 Content-Type 헤더 지정
    }
    try:
        # POST 요청으로 JSON 데이터를 API로 전송
        response = requests.post(api_url, headers=headers, data=json.dumps(data))
        
        # 응답 상태 코드 확인
        if response.status_code == 200 or response.status_code == 201:
            return response.json()  # 응답이 JSON일 경우 반환
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # 예외 처리 (네트워크 오류 등)
        print(f"An error occurred: {e}")
        return None

def put_json_data(api_url, data):
    headers = {
        'Content-Type': 'application/json'  # JSON 데이터를 보낼 때 Content-Type 헤더 지정
    }
    try:
        # POST 요청으로 JSON 데이터를 API로 전송
        response = requests.put(api_url, headers=headers, data=json.dumps(data))
        
        # 응답 상태 코드 확인
        if response.status_code == 200 or response.status_code == 201:
            return response.json()  # 응답이 JSON일 경우 반환
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # 예외 처리 (네트워크 오류 등)
        print(f"An error occurred: {e}")
        return None

def delete_json_data(api_url, data={}):
    headers = {
        'Content-Type': 'application/json'  # JSON 데이터를 보낼 때 Content-Type 헤더 지정
    }
    try:
        # POST 요청으로 JSON 데이터를 API로 전송
        response = requests.delete(api_url, headers=headers, data=json.dumps(data))
        
        # 응답 상태 코드 확인
        if response.status_code == 200 or response.status_code == 201:
            return response.json()  # 응답이 JSON일 경우 반환
        else:
            print(f"Error: Received status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        # 예외 처리 (네트워크 오류 등)
        print(f"An error occurred: {e}")
        return None