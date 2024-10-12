# 중요사항 - 1 : 반드시 \ 를 사용하여 경로를 표시할 것!
# 중요사항 - 2 : 경로의 마지막에 \를 붙이지 말 것!
DOWNLOAD_TEMP_PATH = r"c:\\Users\\sosta\\project\\capstone_proj_sixthsense\\engine\\temp"
CHROM_DRIVER_PATH = r"c:\\Users\\sosta\\project\\capstone_proj_sixthsense\\engine\\chromedriver\\chromedriver-win64\\chromedriver.exe"

SERVER_KEY="CAPSTONE_PROJECT_SIXSENSE_IMAGE_KEY"

SERVER_NAME = r"http://localhost:8080"
READ_READY_PAGE_SERVER_NAME = SERVER_NAME + r"/page/list/ready/by-key/"
UPDATE_PAGE_STATUS_SERVER_NAME = SERVER_NAME + r"/page/update/by-key/"
CREATE_IMAGE_SERVER_NAME = SERVER_NAME + r"/image/save/by-key/"
CREATE_ITEM_SERVER_NAME = SERVER_NAME + r"/item/create/by-page/by-key/"
DELETE_SCANLIST_SERVER_NAME = SERVER_NAME + r"/scan/delete/by-page/by-key/"
CREATE_SCAN_SERVER_NAME = SERVER_NAME + r"/scan/create/by-page/by-item/by-key/"