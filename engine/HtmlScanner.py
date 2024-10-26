from bs4 import BeautifulSoup
from bs4 import Tag
import textwrap
import requests
import DTO

class html_scanner:
    def __init__(self, html_content: str):
        self.html_content = html_content
        self.soup = BeautifulSoup(html_content, 'html.parser')        
    
    # 6.자동 재생 금지
    # 6-1.페이지 진입 시 재생되고 있는 오디오가 있어서는 안된다.
    # 6-2.페이지 진입 시 재생되고 있는 비디오가 있어서는 안된다.(비디오가 소리 없이 재생 중인 경우에는 허용)
    def check_auto_audio(self, selector:str):
        error_message = []
        audio_tag = self.soup.select_one(selector)
        # 규칙 1: caption이 있지만 th가 없는 경우
        scanDTO = DTO.ScanDTO(
            errortype="6.자동 재생 금지",
            errormessage=textwrap.dedent(
                """페이지 진입 시 재생되고 있는 오디오가 있어서는 안된다."""
            )
        )
        itemDTO = DTO.ItemDTO(
            body=audio_tag.prettify(),
            css_selector=selector
        )
        error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        return error_message
    def check_auto_video(self, selector:str):
        error_message = []
        video_tag = self.soup.select_one(selector)
        # 규칙 1: caption이 있지만 th가 없는 경우
        scanDTO = DTO.ScanDTO(
            errortype="6.자동 재생 금지",
            errormessage=textwrap.dedent(
                """페이지 진입 시 재생되고 있는 비디오가 있어서는 안된다.(비디오가 소리 없이 재생 중인 경우에는 허용)"""
            )
        )
        itemDTO = DTO.ItemDTO(
            body=video_tag.prettify(),
            css_selector=selector
        )
        error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        return error_message
    
    # 8.키보드 사용 보장
    # 8-1.키보드를 사용한 이동이 보장되어야 한다.
    def check_tab_loop_item(self, tab_selector, tab_index, tab_img_color, tab_img_gray):
        error_message = []
        print(f"check_tab_loop_item : {tab_selector}")
        itemDTO = DTO.ItemDTO(
            body=self.soup.select_one(tab_selector).prettify(),
            css_selector= tab_selector,
            tabindex=tab_index,
            colorimg=tab_img_color,
            grayimg=tab_img_gray
        )
        scanDTO = DTO.ScanDTO(
            errortype="8.키보드 사용 보장",
            errormessage="키보드를 사용한 초점 이동이 보장되어야 한다."
        )
        error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        return error_message
    def check_tab_loop_item_small(self, tab_selector, tab_index, tab_img_color, tab_img_gray):
        error_message = self.check_tab_loop_item(tab_selector, tab_index, tab_img_color, tab_img_gray)
        for message in error_message:
            message["scan"]["errormessage"] ="키보드를 사용한 이동이 보장되어야 한다.(작은 화면)"
        return error_message
    def check_tab_loop_item_big(self, tab_selector, tab_index, tab_img_color, tab_img_gray):
        error_message = self.check_tab_loop_item(tab_selector, tab_index, tab_img_color, tab_img_gray)
        for message in error_message:
            message["scan"]["errormessage"] ="키보드를 사용한 이동이 보장되어야 한다.(전체 화면)"
        return error_message
    
    # 9.초점 이동
    # 9-1.키보드에 의한 초점은 시각적으로 구별할 수 있어야 한다.
    def check_tab_hidden_item(self, tab_hidden_dict):
        error_message = []
        for hidden_selector, tab_index in tab_hidden_dict.items():
            itemDTO = DTO.ItemDTO(
                body=self.soup.select_one(hidden_selector).prettify(),
                css_selector= hidden_selector,
                tabindex=tab_index,
            )
            scanDTO = DTO.ScanDTO(
                errortype="9.초점 이동",
                errormessage="키보드에 의한 초점은 시각적으로 구별할 수 있어야 한다."
            )
            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        return error_message
    def check_tab_hidden_item_small(self, tab_hidden_dict):
        error_message = self.check_tab_hidden_item(tab_hidden_dict)
        for message in error_message:
            message["scan"]["errormessage"] ="키보드에 의한 초점은 시각적으로 구별할 수 있어야 한다.(작은 화면)"
        return error_message
    def check_tab_hidden_item_big(self, tab_hidden_dict):
        error_message = self.check_tab_hidden_item(tab_hidden_dict)
        for message in error_message:
            message["scan"]["errormessage"] ="키보드에 의한 초점은 시각적으로 구별할 수 있어야 한다.(전체 화면)"
        return error_message
    
    # 14.반복 영역 건너뛰기
    # 14-1.반복되는 영역이 있는 경우, a태그를 활용한 건너뛰기 링크가 마크업상 최 상단에 위치해야 합니다.
    # 14-2.반복 영역 건너뛰기 기능은 키보드 접근 시 화면에 노출되어야 합니다.
    # 14-3.건너뛰기 대상으로 명시된 태그가 실제로 존재해야 합니다.
    def check_skip_link(self, tab_selector_dict, tab_hidden_dict):
        error_message = []
        header_tag = self.soup.find('header')
        # 헤더 태그가 없으면 리턴
        if(not header_tag or not tab_selector_dict):
            return error_message
        
        # dict의 value를 기준으로 key를 정렬
        sorted_tab_select = sorted(tab_selector_dict, key=lambda x: tab_selector_dict[x])
        first_tab_select = sorted_tab_select[0]

        first_tab_tag = self.soup.select_one(first_tab_select)
        href_attribute = first_tab_tag.get('href')
        print(href_attribute)
        
        is_a_tag = first_tab_tag.name == "a"
        is_skip_link = len(href_attribute) > 1 and href_attribute[0] == "#"
        is_first_tab_hidden = first_tab_tag in tab_hidden_dict
        
        # 14-1.반복되는 영역이 있는 경우, a태그를 활용한 건너뛰기 링크가 마크업상 최상단에 위치해야 합니다.
        if(not is_a_tag or not is_skip_link):
            scanDTO = DTO.ScanDTO(
                errortype="14.반복 영역 건너뛰기",
                errormessage="반복되는 영역이 있는 경우, a태그를 활용한 건너뛰기 링크가 마크업상 최상단에 위치해야 합니다."
            )
            itemDTO = DTO.ItemDTO(
                body=header_tag.prettify(),
                css_selector="header"
            )
            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        # 14-2.반복 영역 건너뛰기 기능은 키보드 접근 시 화면에 노출되어야 합니다
        if(is_skip_link and is_first_tab_hidden):
            scanDTO = DTO.ScanDTO(
                errortype="14.반복 영역 건너뛰기",
                errormessage="반복 영역 건너뛰기 기능은 키보드 접근 시 화면에 노출되어야 합니다."
            )
            itemDTO = DTO.ItemDTO(
                body=first_tab_tag.prettify(),
                css_selector=first_tab_select
            )
            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        # 14-3.건너뛰기 대상으로 명시된 태그가 실제로 존재해야 합니다.
        if(is_skip_link and not self.soup.select_one(href_attribute)):
            scanDTO = DTO.ScanDTO(
                errortype="14.반복 영역 건너뛰기",
                errormessage="건너뛰기 대상으로 명시된 태그가 실제로 존재해야 합니다."
            )
            itemDTO = DTO.ItemDTO(
                body=first_tab_tag.prettify(),
                css_selector=first_tab_select
            )
            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        return error_message
    
    # 15.제목 제공
    def check_title(self):
        error_message = []
        
        html_tag = self.soup.find('html')
        head_tag = self.soup.find('head')
        title_tag = self.soup.find('title')
        
        # 15-1. title 태그 찾기
        if not head_tag or not title_tag:
            scanDTO = DTO.ScanDTO(
                errortype="15.제목 제공",
                errormessage="<head> 태그에 페이지 내용을 유추할 수 있는 적절한 <title>을 제공해야 한다."
            )
            if not head_tag:
                itemDTO = DTO.ItemDTO(
                    body=html_tag.prettify(),
                    css_selector="html"
                )
            else:
                itemDTO = DTO.ItemDTO(
                    body=head_tag.prettify(),
                    css_selector="html > head"
                )
            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        
        # 15-2. 모든 iframe 태그 찾기
        iframes = self.soup.find_all('iframe')
        # iframe의 title 속성 유무 확인
        for i, iframe in enumerate(iframes):
            title = iframe.get('title')
            if not title:
                scanDTO = DTO.ScanDTO(
                    errortype="15.제목 제공",
                    errormessage="<iframe>에 적절한 title 속성을 제공해야 한다."
                )
                itemDTO = DTO.ItemDTO(
                    body=iframe.prettify(),
                    css_selector=f"iframe:nth-of-type({i+1})"
                )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        return error_message
    
    # 16.적절한 링크 텍스트
    def check_link_text(self):
        error_message = []
        a_list = self.soup.find_all('a')
        for i, a_tag in enumerate(a_list):
            a_innerHTML = a_tag.contents
            if not a_innerHTML:
                scanDTO = DTO.ScanDTO(
                    errortype="16.적절한 링크 텍스트",
                    errormessage="내부가 비어있는 <a> 태그는 제거하거나 수정해야 한다."
                )
                itemDTO = DTO.ItemDTO(
                    body=a_tag.prettify(),
                    css_selector=f"a:nth-of-type({i+1})"
                )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        return error_message
    
    # 17.기본 언어 표시
    def check_html_lang(self):
        error_message = []
        tag_name = 'html'
        html_tag = self.soup.find(tag_name)
        if not html_tag.get('lang'):
            scanDTO = DTO.ScanDTO(
                errortype="17.기본 언어 표시",
                errormessage="<html> 태그에 주로 사용하는 언어를 lang 속성으로 명시해야 한다."
            )
            itemDTO = DTO.ItemDTO(
                body=html_tag.prettify(),
                css_selector="html"
            )
            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        return error_message
    
    # 18.사용자 요구에 따른 실행
    # 18-1.새 창이라는 것을 알 수 있도록 제공해야 한다.
    def check_new_window_onclick(self):
        error_message = []
        a_list = self.soup.find_all('a')
        for i, a_tag in enumerate(a_list):
            a_target = a_tag.get('target')
            a_title = a_tag.get('title')
            a_onclick = a_tag.get('onclick')
            if a_target == "_blank" and not a_title:
                scanDTO = DTO.ScanDTO(
                    errortype="18.사용자 요구에 따른 실행",
                    errormessage="새 창이라는 것을 알 수 있도록 a 태그에 title을 제공해야 한다."
                )
                itemDTO = DTO.ItemDTO(
                    body=a_tag.prettify(),
                    css_selector=f"a:nth-of-type({i+1})"
                )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
            elif a_onclick and "window.open" in a_onclick:
                scanDTO = DTO.ScanDTO(
                    errortype="18.사용자 요구에 따른 실행",
                    errormessage="새 창이라는 것을 알 수 있도록 a 태그에 title을 제공해야 한다."
                )
                itemDTO = DTO.ItemDTO(
                    body=a_tag.prettify(),
                    css_selector=f"a:nth-of-type({i+1})"
                )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        return error_message
    
    # 20.표의 구성
    # 20-1.표에 <caption>, summary 등을 사용하여 적절한 제목과 요약 정보를 제공한다.
    def check_table_head(self):
        error_message = []
        tables = self.soup.find_all('table')

        for index, table in enumerate(tables, start=1):
            # caption과 th 요소 탐색
            caption = table.find('caption')
            th_elements = table.find_all('th')

            # 규칙 1: caption이 있지만 th가 없는 경우
            if caption and not th_elements:
                scanDTO = DTO.ScanDTO(
                    errortype="20.표의 구성",
                    errormessage=textwrap.dedent(
                        """\
                        <caption>은 발견되었으나, <th>가 발견되지 않았습니다. 
                        해당 <table>이 데이터를 표시하기 위한 표라면, 적절한 제목을 <th>로 제공해야 합니다.
                        디자인을 위한 표라면, <caption>과 <th>를 모두 제거하십시오.\
                        """
                    )
                )
                itemDTO = DTO.ItemDTO(
                    body=table.prettify(),
                    css_selector=f"table:nth-of-type({index})"
                )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
            # 규칙 2: th가 있지만 caption이 없는 경우
            if th_elements and not caption:
                scanDTO = DTO.ScanDTO(
                    errortype="20.표의 구성",
                    errormessage=textwrap.dedent(
                        """\
                        <th>는 발견되었으나, <caption>이 발견되지 않았습니다.
                        해당 <table>이 데이터를 표시하기 위한 표라면, 적절한 설명을 <caption>으로 제공해야 합니다.
                        디자인을 위한 표라면, <caption>과 <th>를 모두 제거하십시오.\
                        """
                    )
                )
                itemDTO = DTO.ItemDTO(
                    body=table.prettify(),
                    css_selector=f"table:nth-of-type({index})"
                )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        return error_message
    
    # 23.마크업 오류 방지
    def check_w3c_markup(self):
        # W3C Markup Validator API에 요청 보내기
        response = requests.post(
            "https://validator.w3.org/nu/?out=json",
            headers={"Content-Type": "text/html; charset=utf-8"},
            data=self.html_content
        )
        # 결과 출력
        if response.status_code == 200 or response.status_code == 201:
            result = response.json()
            error_message = []
            
            except_error = 'Start tag seen without seeing a doctype first. Expected “<!DOCTYPE html>”.'
            detect_keywords = [
                {
                    "keyword" : "Unclosed element ",
                    "errormessage" : "요소의 열고 닫음 : 요소의 열고 닫음이 매칭되도록 제공해야 한다."
                },
                {
                    "keyword" : "violates nesting rules.",
                    "errormessage" : "요소의 중첩 : 요소가 중첩되지 않도록 제공해야 한다."
                },
                {
                    "keyword" : "Duplicate attribute",
                    "errormessage" : "중복된 속성 사용 : 속성이 중복되지 않도록 제공해야 한다."
                },
                {
                    "keyword" : "Duplicate ID",
                    "errormessage" : "id 속성 값 중복 : 페이지 내 id 값이 중복되지 않도록 제공해야 한다."
                },
            ]
            
            for msg in result['messages']: 
                if msg['type'] == 'error' and msg['message'] != except_error:
                    for item in detect_keywords:
                        if item["keyword"] in msg['message']:
                            scanDTO = DTO.ScanDTO(
                                errortype="23.마크업 오류 방지",
                                errormessage=item['errormessage']
                            )
                            itemDTO = DTO.ItemDTO(
                                body=msg['extract'],
                            )
                            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
            return error_message
        return None
    
    
def extract_tag_head(name : str ,tag : Tag):
    taghead = f"<{name}"
    for attr, value in tag.attrs.items():
        taghead += (f' {attr}="{value}"')
    taghead += ">"
    return taghead