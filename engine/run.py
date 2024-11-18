import Api
import Crawler
import HtmlScanner
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import traceback
import ImageDetector
import ImageProcess
import os

def image_detection_process(request_page, width=1920, height=1080):
    crawler = Crawler.crawler()
    try:
        if(request_page["pagetype"] == "TEXT"):
            if(request_page["url"]):
                scanner = HtmlScanner.html_scanner(request_page["htmlbody"])
                request_page["htmlbody"] = scanner.get_refresh_css_html(request_page["url"])
            url = crawler.create_html(request_page["htmlbody"])
            crawler.get(url)
        else:
            crawler.get(request_page["url"])

        # 페이지 읽기 실패하면 Exception raise
        crawler.page_loading_wait()

        # 브라우저 사이즈 설정
        crawler.maximize_window()
        window_size = crawler.window_size

        # scanner에서 html 읽기
        html = crawler.readHTML()
        scanner = HtmlScanner.html_scanner(html)
        # 전체화면 캡쳐
        full_screen_img_path = crawler.capture_full_screenshot()

        imageDetector = ImageDetector.image_detector()
        result = imageDetector.predict(img_path=full_screen_img_path, threshold=0.3)

        pagenation_result = set()
        tab_result = set()
        video_result = set()
        
        for detcet_item in result:
            if(detcet_item['class_name'] == 'pagenation'):
                pagenation_result.add(detcet_item['img_path'])
            if(detcet_item['class_name'] == 'tab'):
                tab_result.add(detcet_item['img_path'])
            if(detcet_item['class_name'] == 'video'):
                video_result.add(detcet_item['img_path'])

        for active_item in result:
            if(active_item['class_name'] == 'pagenation_active'):
                checked_result = []
                for pagenation in pagenation_result:
                    if(ImageProcess.image_matching_check(pagenation, active_item['img_path'])):
                        checked_result.append(pagenation)
                for pagenation in checked_result:
                    pagenation_result.remove(pagenation)

            if(active_item['class_name'] == 'tab_active'):
                checked_result = []
                for tab in tab_result:
                    if(ImageProcess.image_matching_check(tab, active_item['img_path'])):
                        checked_result.append(tab)
                for tab in checked_result:
                    tab_result.remove(tab)

            if(active_item['class_name'] == 'video_cc'):
                checked_result = []
                for video in video_result:
                    if(ImageProcess.image_matching_check(video, active_item['img_path'])):
                        checked_result.append(video)
                for video in checked_result:
                    video_result.remove(video)

        # 02.자막 제공
        video_and_caption_check_list = scanner.check_video_and_caption(video_result)
        for video_and_caption_check in video_and_caption_check_list:
            create_item = Api.post_create_item(request_page["id"], video_and_caption_check["item"])
            create_scan = Api.post_create_scan(request_page["id"], create_item["id"], video_and_caption_check["scan"])

        # 03.색에 무관한 콘텐츠 인식
        color_dependent_contents_check_list = scanner.check_color_dependent_contents(tab_result, pagenation_result)
        for color_dependent_contents_check in color_dependent_contents_check_list:
            create_item = Api.post_create_item(request_page["id"], color_dependent_contents_check["item"])
            create_scan = Api.post_create_scan(request_page["id"], create_item["id"], color_dependent_contents_check["scan"])
        
        # 크롤러 종료
        crawler.close()
    except Exception as e:
        print(traceback.format_exc())
        # 크롤러 종료
        crawler.close()
        return False
    return True

def tab_action_process(request_page, width=1920, height=1080):
    crawler = Crawler.crawler()
    try:
        if(request_page["pagetype"] == "TEXT"):
            if(request_page["url"]):
                scanner = HtmlScanner.html_scanner(request_page["htmlbody"])
                request_page["htmlbody"] = scanner.get_refresh_css_html(request_page["url"])
            url = crawler.create_html(request_page["htmlbody"])
            crawler.get(url)
        else:
            crawler.get(request_page["url"])

        # 페이지 읽기 실패하면 Exception raise
        crawler.page_loading_wait()

        # 브라우저 사이즈 설정
        crawler.maximize_window()
        window_size = crawler.window_size

        # 탭으로 끝까지 이동
        finish_check, tab_selector_dict, tab_hidden_dict = crawler.tab_until_finish()
        # scanner에서 html 읽기
        html = crawler.readHTML()
        scanner = HtmlScanner.html_scanner(html)

        # 8.키보드 사용 보장
        # 8-1.키보드를 사용한 이동이 보장되어야 한다.
        if(not finish_check):
            tab_img_color, tab_img_gray = crawler.capture_focus_element()
            tab_loop_error_check_list = scanner.check_tab_loop_item(
                tab_selector=crawler.get_focus_element_selector(),
                tab_index=len(tab_selector_dict),
                window_size = window_size,
                tab_img_color=tab_img_color, 
                tab_img_gray=tab_img_gray,
            )
            for tab_loop_error_check in tab_loop_error_check_list:
                create_item = Api.post_create_item(request_page["id"], tab_loop_error_check["item"])
                create_scan = Api.post_create_scan(request_page["id"], create_item["id"], tab_loop_error_check["scan"])

        # 9.초점 이동
        # 9-1.키보드에 의한 초점은 시각적으로 구별할 수 있어야 한다.
        tab_hidden_error_check_list = scanner.check_tab_hidden_item(
            tab_hidden_dict = tab_hidden_dict,
            window_size = window_size,
        )
        for tab_hidden_error_check in tab_hidden_error_check_list:
            create_item = Api.post_create_item(request_page["id"], tab_hidden_error_check["item"])
            create_scan = Api.post_create_scan(request_page["id"], create_item["id"], tab_hidden_error_check["scan"])
        
        # 09.초점 이동
        # 09-1.키보드에 의한 초점은 시각적으로 구별할 수 있어야 한다.
        tab_hidden_error_check_list = scanner.check_tab_hidden_item(
            tab_hidden_dict = tab_hidden_dict,
            window_size = window_size
        )
        for tab_hidden_error_check in tab_hidden_error_check_list:
            create_item = Api.post_create_item(request_page["id"], tab_hidden_error_check["item"])
            create_scan = Api.post_create_scan(request_page["id"], create_item["id"], tab_hidden_error_check["scan"])
        
        # 10.조작 가능
        control_img_dict = crawler.all_control_capture()
        control_size_dict =crawler.all_control_size()
        control_size_check_list = scanner.check_control_size(control_img_dict, control_size_dict, window_size)
        for control_size_check in control_size_check_list:
            create_item = Api.post_create_item(request_page["id"], control_size_check["item"])
            create_scan = Api.post_create_scan(request_page["id"], create_item["id"], control_size_check["scan"])
        
        # 14.반복 영역 건너뛰기
        skip_link_error_check_list = scanner.check_skip_link(
            tab_selector_dict=tab_selector_dict,
            tab_hidden_dict=tab_hidden_dict,
            window_size=window_size
        )
        for skip_link_error_check in skip_link_error_check_list:
            create_item = Api.post_create_item(request_page["id"], skip_link_error_check["item"])
            create_scan = Api.post_create_scan(request_page["id"], create_item["id"], skip_link_error_check["scan"])

        # 크롤러 종료
        crawler.close()
    except Exception as e:
        print(traceback.format_exc())
        # 크롤러 종료
        crawler.close()
        return False
    return True

def default_selenium_process(request_page, width=1920, height=1080):
    crawler = Crawler.crawler()
    try:
        if(request_page["pagetype"] == "TEXT"):
            if(request_page["url"]):
                scanner = HtmlScanner.html_scanner(request_page["htmlbody"])
                request_page["htmlbody"] = scanner.get_refresh_css_html(request_page["url"])
            url = crawler.create_html(request_page["htmlbody"])
            crawler.get(url)
        else:
            crawler.get(request_page["url"])

        # 페이지 읽기 실패하면 Exception raise
        crawler.page_loading_wait()
        
        # 브라우저 사이즈 설정
        crawler.maximize_window()
        window_size = crawler.window_size

        # scanner에서 html 읽기
        html = crawler.readHTML()
        scanner = HtmlScanner.html_scanner(html)

        # 06.자동 재생 금지
        audio_check = crawler.auto_loading_audio_check()
        video_check = crawler.auto_loading_video_check()
        
        if(audio_check):
            audio_check_list = scanner.check_auto_audio(audio_check)
            for audio_check in audio_check_list:
                create_item = Api.post_create_item(request_page["id"], audio_check["item"])
                create_scan = Api.post_create_scan(request_page["id"], create_item["id"], audio_check["scan"])
        if(video_check):
            video_check_list = scanner.check_auto_video(video_check)
            for video_check in video_check_list:
                create_item = Api.post_create_item(request_page["id"], video_check["item"])
                create_scan = Api.post_create_scan(request_page["id"], create_item["id"], video_check["scan"])

        # 01.적절한 대체 텍스트 제공
        image_dict = crawler.all_img_capture()
        check_image_alt_list = scanner.check_image_alt(image_dict)
        for check_image_alt in check_image_alt_list:
            create_item = Api.post_create_item(request_page["id"], check_image_alt["item"])
            create_scan = Api.post_create_scan(request_page["id"], create_item["id"], check_image_alt["scan"])
        
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

        # 18.사용자 요구에 따른 실행
        check_new_window_onclick_list = scanner.check_new_window_onclick()
        for check_new_window_onclick in check_new_window_onclick_list:
            create_item = Api.post_create_item(request_page["id"], check_new_window_onclick["item"])
            create_scan = Api.post_create_scan(request_page["id"], create_item["id"], check_new_window_onclick["scan"])

        # 20.표의 구성
        check_table_head_list = scanner.check_table_head()
        for check_table_head in check_table_head_list:
            create_item = Api.post_create_item(request_page["id"], check_table_head["item"])
            create_scan = Api.post_create_scan(request_page["id"], create_item["id"], check_table_head["scan"])
        
        # 21.레이블 제공
        check_input_label_list = scanner.check_input_label()
        for check_input_label in check_input_label_list:
            create_item = Api.post_create_item(request_page["id"], check_input_label["item"])
            create_scan = Api.post_create_scan(request_page["id"], create_item["id"], check_input_label["scan"])

        # 23.마크업 오류 방지
        markup_error_check_list = scanner.check_w3c_markup()
        for markup_error_check in markup_error_check_list:
            create_item = Api.post_create_item(request_page["id"], markup_error_check["item"])
            create_scan = Api.post_create_scan(request_page["id"], create_item["id"], markup_error_check["scan"])
        
        # 크롤러 종료
        crawler.close()
    except Exception as e:
        print(traceback.format_exc())
        # 크롤러 종료
        crawler.close()
        return False
    return True

def run(request_page):
    print(request_page["url"])

    with ThreadPoolExecutor(max_workers=4) as executor:  # 최대 4개의 스레드 사용
        futures = [
            executor.submit(tab_action_process, request_page, 1920, 1080),
            executor.submit(tab_action_process, request_page, 1920 / 3, 1080),
            executor.submit(default_selenium_process, request_page),
            executor.submit(image_detection_process, request_page)
        ]

        results = []
        for future in as_completed(futures):
            try:
                result = future.result()  # 결과 가져오기
                results.append(result)
            except Exception as e:
                print(f"Error occurred: {e}")  # 예외 출력
                results.append({"error": str(e)})  # 에러 내용을 결과에 추가
        print(results)
    
    # 페이지 상태 변경 : RUNNING -> COMPLETE
    if(results[0]
       and results[1]
       and results[2]):
        Api.put_complete_status(request_page["id"])
    else:
        Api.put_error_status(request_page["id"])

if __name__ == '__main__':
    running_tasks = []
    max_process_num = 3
    
    with ProcessPoolExecutor(max_workers=max_process_num) as executor:
        while True:
            next_schedule_list = Api.get_next_schedule()
            for next_schedule in next_schedule_list:
                Api.put_next_schedule(next_schedule["id"])
                Api.put_project_ready_status(next_schedule["project_id"])

            running_tasks = [task for task in running_tasks if not task.done()]
            
            if len(running_tasks) < max_process_num:
                # READY 상태 가져오기
                ready_status_page_list = Api.get_ready_status_page() # READY 상태의 URL을 확인
                if(ready_status_page_list): 
                    request_page = ready_status_page_list[0]
                    run_status_result = Api.put_running_status(request_page["id"])
                    # 해당 페이지의 이전 스캔 결과를 초기화
                    Api.delete_page_scanlist(request_page["id"])

                    future = executor.submit(run, request_page)
                    running_tasks.append(future)
            time.sleep(2)