from bs4 import BeautifulSoup
from bs4 import Tag
import requests
import DTO

class html_scanner:
    def __init__(self, html_content: str):
        self.html_content = html_content
        self.soup = BeautifulSoup(html_content, 'html.parser')        
    
    # 9.초점 이동
    # 9-1.키보드를 사용한 초점 이동이 보장되어야 한다.
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
            errortype="9.초점 이동",
            errormessage="키보드를 사용한 초점 이동이 보장되어야 한다."
        )
        error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        return error_message
    def check_tab_loop_item_small(self, tab_selector, tab_index, tab_img_color, tab_img_gray):
        error_message = self.check_tab_loop_item(tab_selector, tab_index, tab_img_color, tab_img_gray)
        for message in error_message:
            message["scan"]["errormessage"] ="키보드를 사용한 초점 이동이 보장되어야 한다.(작은 화면)"
        return error_message
    def check_tab_loop_item_big(self, tab_selector, tab_index, tab_img_color, tab_img_gray):
        error_message = self.check_tab_loop_item(tab_selector, tab_index, tab_img_color, tab_img_gray)
        for message in error_message:
            message["scan"]["errormessage"] ="키보드를 사용한 초점 이동이 보장되어야 한다.(전체 화면)"
        return error_message
    # 9-2.키보드에 의한 초점은 시각적으로 구별할 수 있어야 한다.
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
    # 14-2.반복 영역 건너뛰기 기능은 키보드 접근 시 화면에 노출되어야 합니다
    def check_skip_link(self, tab_selector_dict, tab_hidden_dict):
        error_message = []
        header_tag = self.soup.find('header')
        # 헤더 태그가 없으면 리턴
        if(not header_tag):
            return error_message
        
        # dict의 value를 기준으로 key를 정렬
        sorted_tab_select = sorted(tab_selector_dict, key=lambda x: tab_selector_dict[x])
        first_tab_select = sorted_tab_select[0]

        first_tab_tag = self.soup.select(first_tab_select)[0]
        href_attribute = first_tab_tag.get('href')
        
        is_a_tag = first_tab_tag.name == "a"
        is_skip_link = href_attribute[0] == "#" and len(href_attribute) > 1
        
        # 14-1.반복되는 영역이 있는 경우, a태그를 활용한 건너뛰기 링크가 마크업상 최상단에 위치해야 합니다.
        if(not is_a_tag or not is_skip_link):
            scanDTO = DTO.ScanDTO(
                errortype="14.반복 영역 건너뛰기",
                errormessage="반복되는 영역이 있는 경우, a태그를 활용한 건너뛰기 링크가 마크업상 최 상단에 위치해야 합니다."
            )
            itemDTO = DTO.ItemDTO(
                body=header_tag.prettify(),
                css_selector="header"
            )
            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        # 14-2.반복 영역 건너뛰기 기능은 키보드 접근 시 화면에 노출되어야 합니다
        elif(first_tab_tag in tab_hidden_dict):
            scanDTO = DTO.ScanDTO(
                errortype="14.반복 영역 건너뛰기",
                errormessage="반복 영역 건너뛰기 기능은 키보드 접근 시 화면에 노출되어야 합니다."
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
            a_title = a_tag.get('title')
            if not a_innerHTML and not a_title:
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