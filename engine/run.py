import Api
import Crawler
import HtmlScanner
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
import traceback
import ImageDetector
import ImageProcess
import os

def image_detection_process(request_page):
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
        crawler.update_height_max()

        # scanner에서 html 읽기
        html = crawler.readHTML()
        scanner = HtmlScanner.html_scanner(html)
        
        # 전체화면 캡쳐
        full_screen_img_path_before = crawler.capture_screenshot()
        time.sleep(5)
        full_screen_img_path_after = crawler.capture_screenshot()

        # 이미지 분석 모델
        imageDetector = ImageDetector.image_detector()
        result = imageDetector.predict(img_path=full_screen_img_path_before, threshold=0.5)

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

        # 슬라이드 이미지 탐색
        auto_changed_image_list = ImageProcess.find_and_save_differences_with_connected_regions(
            image1_path=full_screen_img_path_before,
            image2_path=full_screen_img_path_after,
            output_dir=crawler.download_path
        )
        # 명도 대비 오류 텍스트
        error_text_image_dict = crawler.get_contrast_error_text_img_dict()

        # 02.자막 제공
        video_and_caption_check_list = scanner.check_video_and_caption(
            request_id=request_page["id"], 
            video_image_list=video_result
        )
        # 03.색에 무관한 콘텐츠 인식
        color_dependent_contents_check_list = scanner.check_color_dependent_contents(
            request_id=request_page["id"],
            tab_result=tab_result,
            pagenation_result=pagenation_result
        )
        # 05.텍스트 콘텐츠의 명도 대비
        text_image_contrast_check_list = scanner.check_text_image_contrast(
            request_id=request_page["id"],
            text_image_error_dict=error_text_image_dict
        )
        # 12.정지 기능 제공
        auto_changed_image_check_list = scanner.check_auto_changed_contents(
            request_id=request_page["id"],
            auto_changed_image_list=auto_changed_image_list
        )

        # 크롤러 종료
        crawler.close()
    except Exception as e:
        print(traceback.format_exc())
        # 크롤러 종료
        crawler.close()
        return False
    return True

def tab_action_process(request_page, width_rate=1.0):
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
        crawler.set_width_rate(width_rate)
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
                request_id=request_page["id"],
                tab_selector=crawler.get_focus_element_selector(),
                tab_index=len(tab_selector_dict),
                window_size = window_size,
                tab_img_color=tab_img_color, 
                tab_img_gray=tab_img_gray,
            )

        # 9.초점 이동
        # 9-1.키보드에 의한 초점은 시각적으로 구별할 수 있어야 한다.
        tab_hidden_error_check_list = scanner.check_tab_hidden_item(
            request_id=request_page["id"], 
            tab_hidden_dict = tab_hidden_dict,
            window_size = window_size,
        )
        
        # 09.초점 이동
        # 09-1.키보드에 의한 초점은 시각적으로 구별할 수 있어야 한다.
        tab_hidden_error_check_list = scanner.check_tab_hidden_item(
            request_id=request_page["id"], 
            tab_hidden_dict = tab_hidden_dict,
            window_size = window_size
        )
        
        # 10.조작 가능
        control_img_dict = crawler.all_control_capture()
        control_size_dict =crawler.all_control_size()
        control_size_check_list = scanner.check_control_size(
            request_id=request_page["id"], 
            control_img_dict=control_img_dict, 
            control_size_dict=control_size_dict, 
            window_size=window_size
        )
        
        # 14.반복 영역 건너뛰기
        skip_link_error_check_list = scanner.check_skip_link(
            request_id=request_page["id"], 
            tab_selector_dict=tab_selector_dict,
            tab_hidden_dict=tab_hidden_dict,
            window_size=window_size
        )

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
            audio_check_list = scanner.check_auto_audio(
                request_id=request_page["id"], 
                selector=audio_check
            )
        if(video_check):
            video_check_list = scanner.check_auto_video(
                request_id=request_page["id"], 
                selector=video_check
            )

        # 01.적절한 대체 텍스트 제공
        image_dict = crawler.all_img_capture()
        check_image_alt_list = scanner.check_image_alt(
            request_id=request_page["id"], 
            image_dict=image_dict
        )
        
        # 04.명확한 지시 사항 제공
        required_id_and_info = crawler.get_required_id_and_info()
        scanner.check_required_id_and_info(
            request_id=request_page["id"], 
            id_and_info_dict=required_id_and_info
        )

        # 15.제목 제공
        title_error_check_list = scanner.check_title(request_id=request_page["id"])

        # 16.적절한 링크 텍스트
        check_link_text_list = scanner.check_link_text(request_id=request_page["id"])
            
        # 17.기본 언어 표시
        check_html_lang_list = scanner.check_html_lang(request_id=request_page["id"])

        # 18.사용자 요구에 따른 실행
        check_new_window_onclick_list = scanner.check_new_window_onclick(request_id=request_page["id"])

        # 20.표의 구성
        check_table_head_list = scanner.check_table_head(request_id=request_page["id"])
        
        # 21.레이블 제공
        check_input_label_list = scanner.check_input_label(request_id=request_page["id"])

        # 23.마크업 오류 방지
        markup_error_check_list = scanner.check_w3c_markup(request_id=request_page["id"])
        
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
            executor.submit(tab_action_process, request_page, 1.0),
            executor.submit(tab_action_process, request_page, 0.33),
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
       and results[2]
       and results[3]):
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