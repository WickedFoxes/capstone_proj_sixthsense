import config

import sys
import os
import json
import requests
import Api
import Crawler
import HtmlScanner
import DTO
from requests_toolbelt.multipart.encoder import MultipartEncoder


# READY 상태 가져오기
data = Api.get_ready_status_page()
if(len(data) == 0): 
    sys.exit()

for request_page in data:
    print(request_page)
    # 페이지 상태 변경 : READY -> RUNNING
    Api.put_running_status(request_page["id"])
    # 해당 페이지의 이전 스캔 결과를 초기화
    Api.delete_page_scanlist(request_page["id"])

    # 크롤러를 사용하여 HTML 수집
    # 작은 화면에서 실행
    crawler = Crawler.crawler()
    crawler.get(request_page["url"])
    window_size_fullscreen = crawler.driver.get_window_size()
    print(window_size_fullscreen)
    crawler.driver.set_window_size(window_size_fullscreen["width"]/3, window_size_fullscreen["height"])
    
    if crawler.page_loading_wait():
        # scanner에서 html 읽기
        html = crawler.readHTML()
        scanner = HtmlScanner.html_scanner(html)
        
        # 탭으로 끝까지 이동
        finish_check, tab_selector_dict, tab_hidden_dict = crawler.tab_until_finish()
        
        # 9.초점 이동
        # 9-1.키보드를 사용한 초점 이동이 보장되어야 한다.
        if(not finish_check):
            tab_img_color, tab_img_gray = crawler.capture_focus_element()
            color_img_res = Api.post_create_img_item(tab_img_color)
            gray_img_res = Api.post_create_img_item(tab_img_gray)
            tab_loop_error_check_list = scanner.check_tab_loop_item_small(
                tab_selector=crawler.get_focus_element_selector(),
                tab_index=len(tab_selector_dict),
                tab_img_color=color_img_res["name"],
                tab_img_gray=gray_img_res["name"],
            )
            for tab_loop_error_check in tab_loop_error_check_list:
                create_item = Api.post_create_item(request_page["id"], tab_loop_error_check["item"])
                create_scan = Api.post_create_scan(request_page["id"], create_item["id"], tab_loop_error_check["scan"])
        
        # 9.초점 이동
        # 9-2.키보드에 의한 초점은 시각적으로 구별할 수 있어야 한다.
        tab_hidden_error_check_list = scanner.check_tab_hidden_item_small(tab_hidden_dict)
        for tab_hidden_error_check in tab_hidden_error_check_list:
            create_item = Api.post_create_item(request_page["id"], tab_hidden_error_check["item"])
            create_scan = Api.post_create_scan(request_page["id"], create_item["id"], tab_hidden_error_check["scan"])
    
    # 크롤러 종료
    crawler.close()
    
    # 크롤러를 사용하여 HTML 수집
    # 큰 화면에서 실행
    crawler = Crawler.crawler()
    crawler.get(request_page["url"])
    window_size_fullscreen = crawler.driver.get_window_size()
    crawler.driver.set_window_size(window_size_fullscreen["width"], window_size_fullscreen["height"])
    
    if(crawler.page_loading_wait()):
        # scanner에서 html 읽기
        html = crawler.readHTML()
        scanner = HtmlScanner.html_scanner(html)
        
        # 탭으로 끝까지 이동
        finish_check, tab_selector_dict, tab_hidden_dict = crawler.tab_until_finish()
        
        # 9.초점 이동
        # 9-1.키보드를 사용한 초점 이동이 보장되어야 한다.
        if(not finish_check):
            tab_img_color, tab_img_gray = crawler.capture_focus_element()
            color_img_res = Api.post_create_img_item(tab_img_color)
            gray_img_res = Api.post_create_img_item(tab_img_gray)
            tab_loop_error_check_list = scanner.check_tab_loop_item_big(
                tab_selector=crawler.get_focus_element_selector(),
                tab_index=len(tab_selector_dict),
                tab_img_color=color_img_res["name"],
                tab_img_gray=gray_img_res["name"],
            )
            for tab_loop_error_check in tab_loop_error_check_list:
                create_item = Api.post_create_item(request_page["id"], tab_loop_error_check["item"])
                create_scan = Api.post_create_scan(request_page["id"], create_item["id"], tab_loop_error_check["scan"])
        
        # 9.초점 이동
        # 9-2.키보드에 의한 초점은 시각적으로 구별할 수 있어야 한다.
        tab_hidden_error_check_list = scanner.check_tab_hidden_item_big(tab_hidden_dict)
        for tab_hidden_error_check in tab_hidden_error_check_list:
            create_item = Api.post_create_item(request_page["id"], tab_hidden_error_check["item"])
            create_scan = Api.post_create_scan(request_page["id"], create_item["id"], tab_hidden_error_check["scan"])
        
        # 14.반복 영역 건너뛰기
        skip_link_error_check_list = scanner.check_skip_link(
            tab_selector_dict=tab_selector_dict,
            tab_hidden_dict=tab_hidden_dict
        )
        for skip_link_error_check in skip_link_error_check_list:
            create_item = Api.post_create_item(request_page["id"], skip_link_error_check["item"])
            create_scan = Api.post_create_scan(request_page["id"], create_item["id"], skip_link_error_check["scan"])
        
        # 15.제목 제공
        title_error_check_list = scanner.check_title()
        for title_error_check in title_error_check_list:
            create_item = Api.post_create_item(request_page["id"], title_error_check["item"])
            create_scan = Api.post_create_scan(request_page["id"], create_item["id"], title_error_check["scan"])

        # 16.적절한 링크 텍스트
        check_link_text_list = scanner.check_link_text()
        for check_link_text in check_link_text_list:
            create_item = Api.post_create_item(request_page["id"], check_link_text["item"])
            create_scan = Api.post_create_scan(request_page["id"], create_item["id"], check_link_text["scan"])
            
        # 17.기본 언어 표시
        check_html_lang_list = scanner.check_html_lang()
        for check_html_lang in check_html_lang_list:
            create_item = Api.post_create_item(request_page["id"], check_html_lang["item"])
            create_scan = Api.post_create_scan(request_page["id"], create_item["id"], check_html_lang["scan"])

        # 23.마크업 오류 방지
        markup_error_check_list = scanner.check_w3c_markup()
        for markup_error_check in markup_error_check_list:
            create_item = Api.post_create_item(request_page["id"], markup_error_check["item"])
            create_scan = Api.post_create_scan(request_page["id"], create_item["id"], markup_error_check["scan"])
    
    # 크롤러 종료
    crawler.close()
    # 페이지 상태 변경 : RUNNING -> COMPLETE
    Api.put_complete_status(request_page["id"])