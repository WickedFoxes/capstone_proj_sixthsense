import config

import sys
import os
import json
import requests
import Api
import Crawler
import HtmlScanner
from requests_toolbelt.multipart.encoder import MultipartEncoder


# READY 상태 가져오기
data = Api.get_ready_status_page()
if(len(data) == 0): sys.exit()

for request_page in data:
    print(request_page)
    # 페이지 상태 변경 : READY -> RUNNING
    Api.put_running_status(request_page["id"])
    # 해당 페이지의 이전 스캔 결과를 초기화
    Api.delete_page_scanlist(request_page["id"])

    # 크롤러를 사용하여 HTML 수집
    crawler = Crawler.crawler()
    crawler.get(request_page["url"])
    html = crawler.readHTML()
    crawler.close()

    scanner = HtmlScanner.html_scanner(html)

    # 15.제목 제공
    title_error_check_list = scanner.check_title()
    for title_error_check in title_error_check_list:
        create_item = Api.post_create_item(request_page["id"], title_error_check["item"])
        create_scan = Api.post_create_scan(request_page["id"], create_item["id"], title_error_check["scan"])

    # 17. 기본 언어 표시
    check_html_lang_list = scanner.check_html_lang()
    for check_html_lang in check_html_lang_list:
        create_item = Api.post_create_item(request_page["id"], check_html_lang["item"])
        create_scan = Api.post_create_scan(request_page["id"], create_item["id"], check_html_lang["scan"])

    # 23.마크업 오류 방지
    markup_error_check_list = scanner.check_w3c_markup()
    for markup_error_check in markup_error_check_list:
        create_item = Api.post_create_item(request_page["id"], markup_error_check["item"])
        create_scan = Api.post_create_scan(request_page["id"], create_item["id"], markup_error_check["scan"])

    # 페이지 상태 변경 : RUNNING -> COMPLETE
    Api.put_complete_status(request_page["id"])