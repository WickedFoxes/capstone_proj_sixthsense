from bs4 import BeautifulSoup
import requests
import DTO

class html_scanner:
    def __init__(self, html_content: str):
        self.html_content = html_content
        self.soup = BeautifulSoup(html_content, 'html.parser')        
    
    # 15.제목 제공
    def check_title(self):
        error_message = []
        
        head_tag = self.soup.find('head')
        title_tag = self.soup.find('title')
        
        # 15-1. title 태그 찾기
        if not title_tag:
            scanDTO = DTO.ScanDTO(
                errortype="15.제목 제공",
                errormessage="<head> 태그에 페이지 내용을 유추할 수 있는 적절한 <title>을 제공해야 한다."
            )
            itemDTO = DTO.ItemDTO(
                body=head_tag.prettify(),
            )
            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        
        # 15-2. 모든 iframe 태그 찾기
        iframes = self.soup.find_all('iframe')
        # iframe의 title 속성 유무 확인
        for iframe in iframes:
            title = iframe.get('title')
            if not title:
                scanDTO = DTO.ScanDTO(
                    errortype="15.제목 제공",
                    errormessage="<iframe>에 적절한 title 속성을 제공해야 한다."
                )
                itemDTO = DTO.ItemDTO(
                    body=iframe.prettify(),
                )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        return error_message
    
    # 17. 기본 언어 표시
    def check_html_lang(self):
        error_message = []
        html_tag = self.soup.find('html')
        if not html_tag.get('lang'):
            tagbody = "<html"
            for attr, value in html_tag.attrs.items():
                tagbody += (f' {attr}="{value}"')
            tagbody += ">"
            
            scanDTO = DTO.ScanDTO(
                errortype="17.기본 언어 표시",
                errormessage="<html> 태그에 페주로 사용하는 언어를 lang 속성으로 명시해야 한다."
            )
            itemDTO = DTO.ItemDTO(
                body=tagbody,
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
        if response.status_code == 200:
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