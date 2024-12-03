from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from bs4 import Tag
import Api
import textwrap
import requests
import DTO

class html_scanner:
    def __init__(self, html_content: str):
        self.html_content = html_content
        self.soup = BeautifulSoup(html_content, 'html.parser')        
    
    def get_refresh_css_html(self, base_url):
        parsed_url = urlparse(base_url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}/"
        
        # src, href를 가진 요소 찾기
        links = self.soup.select('[src], [href]')

        # href의 도메인이 비어 있는 경우 수정
        for link in links:
            if link.has_attr('href'):
                href = link['href']
                # URL이 절대 경로가 아니라면 도메인 추가
                if href.startswith("/"):
                    link['href'] = urljoin(domain, href)  # 도메인을 추가하여 절대 URL로 변환
            if link.has_attr('src'):
                src = link['src']
                # URL이 절대 경로가 아니라면 도메인 추가
                if src.startswith("/"):
                    link['src'] = urljoin(domain, src)  # 도메인을 추가하여 절대 URL로 변환

        # 수정된 HTML 출력
        return self.soup.prettify()


    # 01.적절한 대체 텍스트 제공
    # 01-1.<img>, <input type="image">, <area> 의 alt에는 적절한 대체 텍스트를 제공한다.
    def check_image_alt(self, 
                        request_id,
                        image_dict):
        # 결과 저장용 리스트
        error_message = []
        # 검사 대상 입력 필드
        img_fields = self.soup.find_all('img')
        input_fields = self.soup.find_all(['input'], {'type': lambda x: x in ['image']})
        area_fields = self.soup.find_all('area')
        
        # 각 입력 필드에 대해 검사
        for index, field in enumerate(img_fields, start=1):
            img_alt = field.get('alt', None)
            # 필드별 상태 설정
            if not img_alt:
                scanDTO = DTO.ScanDTO(
                    errortype="01.적절한 대체 텍스트 제공",
                    errormessage=textwrap.dedent(
                        """\
                        <img>의 alt에는 적절한 대체 텍스트를 제공해야 합니다.
                        (장식 또는 꾸밈 목적 등의 의미 없는 이미지는 대체 텍스트를 제공하지 않아도 됩니다.)\
                        """
                    ),
                    erroroption="WARNING"
                )
                css_selector = self.get_css_path(field)
                
                itemDTO = DTO.ItemDTO(
                    body=field.prettify(),
                    css_selector=css_selector,
                )
                if(css_selector in image_dict and image_dict[css_selector]['color_img_path']):
                    color_img_res = Api.post_create_img_item(image_dict[css_selector]['color_img_path'])
                    gray_img_res = Api.post_create_img_item(image_dict[css_selector]['gray_img_path'])
                    itemDTO = DTO.ItemDTO(
                        body=field.prettify(),
                        css_selector=css_selector,
                        colorimg=color_img_res['name'],
                        grayimg=gray_img_res['name']
                    )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        
        # 각 입력 필드에 대해 검사
        for index, field in enumerate(input_fields, start=1):
            img_alt = field.get('alt', None)
            # 필드별 상태 설정
            if not img_alt:
                scanDTO = DTO.ScanDTO(
                    errortype="01.적절한 대체 텍스트 제공",
                    errormessage=textwrap.dedent(
                        """\
                        <input[type="image"]>의 alt에는 적절한 대체 텍스트를 제공해야 합니다.
                        (장식 또는 꾸밈 목적 등의 의미 없는 이미지는 대체 텍스트를 제공하지 않아도 됩니다.)\
                        """
                    ),
                    erroroption="WARNING"
                )
                css_selector = self.get_css_path(field)
                itemDTO = DTO.ItemDTO(
                    body=field.prettify(),
                    css_selector=css_selector,
                )
                if(css_selector in image_dict and image_dict[css_selector]['color_img_path']):
                    color_img_res = Api.post_create_img_item(image_dict[css_selector]['color_img_path'])
                    gray_img_res = Api.post_create_img_item(image_dict[css_selector]['gray_img_path'])
                    itemDTO = DTO.ItemDTO(
                        body=field.prettify(),
                        css_selector=css_selector,
                        colorimg=color_img_res['name'],
                        grayimg=gray_img_res['name']
                    )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        # 각 입력 필드에 대해 검사
        for index, field in enumerate(area_fields, start=1):
            img_alt = field.get('alt', None)
            # 필드별 상태 설정
            if not img_alt:
                scanDTO = DTO.ScanDTO(
                    errortype="01.적절한 대체 텍스트 제공",
                    errormessage=textwrap.dedent(
                        """\
                        <area>의 alt에는 적절한 대체 텍스트를 제공해야 합니다.
                        (장식 또는 꾸밈 목적 등의 의미 없는 이미지는 대체 텍스트를 제공하지 않아도 됩니다.)\
                        """
                    ),
                    erroroption="WARNING"
                )
                css_selector = self.get_css_path(field)
                itemDTO = DTO.ItemDTO(
                    body=field.prettify(),
                    css_selector=css_selector,
                )
                if(css_selector in image_dict and image_dict[css_selector]['color_img_path']):
                    color_img_res = Api.post_create_img_item(image_dict[css_selector]['color_img_path'])
                    gray_img_res = Api.post_create_img_item(image_dict[css_selector]['gray_img_path'])
                    itemDTO = DTO.ItemDTO(
                        body=field.prettify(),
                        css_selector=css_selector,
                        colorimg=color_img_res['name'],
                        grayimg=gray_img_res['name']
                    )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        
        for error_item in error_message:
            create_item = Api.post_create_item(request_id, error_item["item"])
            create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
        return error_message

    # 2. 자막 제공
    def check_video_and_caption(self, 
                                request_id, 
                                video_image_list):
        error_message = []
        for video_image in video_image_list:
            # video가 있으나, video_cc가 없는 것으로 추정되는 경우
            scanDTO = DTO.ScanDTO(
                errortype="02.자막 제공",
                errormessage=textwrap.dedent(
                    """설명이나 자막이 없이 제공되고 있는 동영상이 있는 것으로 추정됩니다."""
                ),
                erroroption="WARNING"
            )
            img_res = Api.post_create_img_item(video_image)
            itemDTO = DTO.ItemDTO(
                body="",
                css_selector="",
                grayimg=img_res['name'],
                colorimg=img_res['name']
            )
            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        
        for error_item in error_message:
            create_item = Api.post_create_item(request_id, error_item["item"])
            create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
        return error_message

    # 3. 색에 무관한 콘텐츠 인식
    def check_color_dependent_contents(self, 
                                       request_id, 
                                       tab_result, 
                                       pagenation_result):
        error_message = []

        color_dependent_image_list = []
        for image in tab_result:
            color_dependent_image_list.append(image)
        for image in pagenation_result:
            color_dependent_image_list.append(image)

        for color_dependent_image in color_dependent_image_list:
            # 색이 아닌 패턴, 굵기, 모양, 테두리 등의 방법으로 구분되는 요소가 없는 것으로 추정되는 경우
            scanDTO = DTO.ScanDTO(
                errortype="03.색에 무관한 콘텐츠 인식",
                errormessage=textwrap.dedent(
                    """색이 아닌 패턴, 굵기, 모양, 테두리 등의 방법으로 구분되는 요소가 없는 것으로 추정됩니다."""
                ),
                erroroption="WARNING"
            )
            img_res = Api.post_create_img_item(color_dependent_image)
            itemDTO = DTO.ItemDTO(
                body="",
                css_selector="",
                grayimg=img_res['name'],
                colorimg=img_res['name']
            )
            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        
        for error_item in error_message:
            create_item = Api.post_create_item(request_id, error_item["item"])
            create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
        return error_message


    # 4. 명확한 지시 사항 제공
    # 모양으로만 정보를 제공해서는 안된다.
    def check_required_id_and_info(self,
                                  request_id,
                                  id_and_info_dict):
        error_message = []

        if not id_and_info_dict["check"]:
            scanDTO = DTO.ScanDTO(
                errortype="04.명확한 지시 사항 제공",
                errormessage=textwrap.dedent(
                    f"""\
                    '*' 모양으로만 정보를 제공해서는 안됩니다. 
                    '* 표시는 필수 입력 사항입니다.'와 같은 문구를 제공하시요.\
                    """
                ),
                erroroption="ERROR"
            )
            color_img_res = Api.post_create_img_item(id_and_info_dict["color_img_path"])
            gray_img_res = Api.post_create_img_item(id_and_info_dict["gray_img_path"])
            body_element = self.soup.select_one(id_and_info_dict["css_path"])

            itemDTO = DTO.ItemDTO(
                body=body_element.prettify(),
                css_selector=id_and_info_dict["css_path"],
                grayimg=gray_img_res['name'],
                colorimg=color_img_res['name']
            )
            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        
        for error_item in error_message:
            create_item = Api.post_create_item(request_id, error_item["item"])
            create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
        return error_message   


    # 5.텍스트 콘텐츠의 명도 대비
    # 텍스트 콘텐츠와 배경 간의 명도 대비는 4.5 대 1 이상이어야 한다.
    def check_text_image_contrast(self,
                                  request_id,
                                  text_image_error_dict):
        error_message = []
        for css_path, item_dict in text_image_error_dict.items():
            scanDTO = DTO.ScanDTO(
                errortype="05.텍스트 콘텐츠의 명도 대비",
                errormessage=textwrap.dedent(
                    f"""텍스트 콘텐츠와 배경 간의 명도 대비는 4.5 대 1 이상이어야 합니다.(현재 {round(item_dict["ratio"],2)})"""
                ),
                erroroption="WARNING"
            )
            color_img_res = Api.post_create_img_item(item_dict["color_img_path"])
            gray_img_res = Api.post_create_img_item(item_dict["gray_img_path"])
            itemDTO = DTO.ItemDTO(
                body="",
                css_selector=css_path,
                grayimg=gray_img_res['name'],
                colorimg=color_img_res['name']
            )
            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        
        for error_item in error_message:
            create_item = Api.post_create_item(request_id, error_item["item"])
            create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
        return error_message        


    # 6.자동 재생 금지
    # 6-1.페이지 진입 시 재생되고 있는 오디오가 있어서는 안된다.
    # 6-2.페이지 진입 시 재생되고 있는 비디오가 있어서는 안된다.(비디오가 소리 없이 재생 중인 경우에는 허용)
    def check_auto_audio(self, 
                         request_id,
                         selector:str):
        error_message = []
        audio_tag = self.soup.select_one(selector)
        # 규칙 1: caption이 있지만 th가 없는 경우
        scanDTO = DTO.ScanDTO(
            errortype="06.자동 재생 금지",
            errormessage=textwrap.dedent(
                """페이지 진입 시 재생되고 있는 오디오가 있어서는 안됩니다."""
            ),
            erroroption="ERROR"
        )
        
        itemDTO = DTO.ItemDTO(
            body=audio_tag.prettify(),
            css_selector=selector
        )
        error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        for error_item in error_message:
            create_item = Api.post_create_item(request_id, error_item["item"])
            create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
        return error_message
    def check_auto_video(self, 
                         request_id,
                         selector:str):
        error_message = []
        video_tag = self.soup.select_one(selector)
        # 규칙 1: caption이 있지만 th가 없는 경우
        scanDTO = DTO.ScanDTO(
            errortype="06.자동 재생 금지",
            errormessage=textwrap.dedent(
                """페이지 진입 시 재생되고 있는 비디오가 있어서는 안됩니다.(비디오가 소리 없이 재생 중인 경우에는 허용)"""
            ),
            erroroption="WARNING"
        )
        itemDTO = DTO.ItemDTO(
            body=video_tag.prettify(),
            css_selector=selector
        )
        error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        for error_item in error_message:
            create_item = Api.post_create_item(request_id, error_item["item"])
            create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
        return error_message
    
    # 8.키보드 사용 보장
    # 8-1.키보드를 사용한 이동이 보장되어야 한다.
    def check_tab_loop_item(self, 
                            request_id,
                            tab_selector, 
                            tab_index, 
                            window_size,
                            tab_img_color, 
                            tab_img_gray):
        error_message = []

        itemDTO = DTO.ItemDTO(
            body=self.soup.select_one(tab_selector).prettify(),
            css_selector= tab_selector,
            tabindex=tab_index,
        )        
        if(tab_img_color):
            color_img_res = Api.post_create_img_item(tab_img_color)
            gray_img_res = Api.post_create_img_item(tab_img_gray)
            itemDTO = DTO.ItemDTO(
                body=self.soup.select_one(tab_selector).prettify(),
                css_selector= tab_selector,
                tabindex=tab_index,
                colorimg=color_img_res['name'],
                grayimg=gray_img_res['name']
            )
        scanDTO = DTO.ScanDTO(
            errortype=f"08.키보드 사용 보장(width:{window_size["width"]}px, height:{window_size["height"]}px)",
            errormessage="키보드를 사용한 초점 이동이 보장되어야 한다.",
            erroroption="ERROR"
        )
        error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        for error_item in error_message:
            create_item = Api.post_create_item(request_id, error_item["item"])
            create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
        return error_message
    
    # 9.초점 이동
    # 9-1.키보드에 의한 초점은 시각적으로 구별할 수 있어야 한다.
    def check_tab_hidden_item(self, 
                              request_id,
                              tab_hidden_dict,
                              window_size):
        error_message = []
        for hidden_selector, tab_index in tab_hidden_dict.items():
            itemDTO = DTO.ItemDTO(
                body=self.soup.select_one(hidden_selector).prettify(),
                css_selector= hidden_selector,
                tabindex=tab_index,
            )
            scanDTO = DTO.ScanDTO(
                errortype=f"09.초점 이동(width:{window_size["width"]}px, height:{window_size["height"]}px)",
                errormessage="키보드에 의한 초점은 시각적으로 구별할 수 있어야 한다.",
                erroroption="ERROR"
            )
            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        for error_item in error_message:
            create_item = Api.post_create_item(request_id, error_item["item"])
            create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
        return error_message

    # 10.조작 가능
    def check_control_size(self, 
                           request_id,
                           control_img_dict, 
                           control_size_dict, 
                           window_size):
        # 결과 저장용 리스트
        error_message = []
        
        # 픽셀을 mm로 변환하는 함수 (기본적인 변환 비율 설정)
        PIXEL_TO_MM = 0.264583  # 1px ≈ 0.264583 mm (일반적인 변환 비율)
        MIN_DIAGONAL_MM = 6 / PIXEL_TO_MM  # 대각선 길이 기준 (픽셀 단위로 변환)
        
        # 검사 대상 입력 필드
        input_fields = self.soup.find_all(['input'], {'type': lambda x: x not in ['hidden', 'image']})
        textarea_fields = self.soup.find_all(['textarea'])
        button_fields = self.soup.find_all(['button'])

        # 각 입력 필드에 대해 검사
        for index, field in enumerate(input_fields, start=1):
            css_selector = self.get_css_path(field)
            
            # 필드별 상태 설정
            if(css_selector in control_size_dict and control_size_dict[css_selector]['diagonal'] <= MIN_DIAGONAL_MM):
                diagonal = control_size_dict[css_selector]['diagonal']
                scanDTO = DTO.ScanDTO(
                    errortype=f"10.조작 가능(width:{window_size["width"]}px, height:{window_size["height"]}px)",
                    errormessage=textwrap.dedent(
                        f"""컨트롤의 크기는 대각선 길이가 6mm 이상이 되도록 제공해야 합니다. (현재 {round(diagonal*PIXEL_TO_MM, 2)}mm)"""
                    ),
                    erroroption="ERROR"
                )
                itemDTO = DTO.ItemDTO(
                    body=field.prettify(),
                    css_selector=css_selector,
                )
                if(css_selector in control_img_dict and control_img_dict[css_selector]['color_img_path']):
                    color_img_res = Api.post_create_img_item(control_img_dict[css_selector]['color_img_path'])
                    gray_img_res = Api.post_create_img_item(control_img_dict[css_selector]['gray_img_path'])
                    itemDTO = DTO.ItemDTO(
                        body=field.prettify(),
                        css_selector=css_selector,
                        colorimg=color_img_res['name'],
                        grayimg=gray_img_res['name']
                    )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        # 각 입력 필드에 대해 검사
        for index, field in enumerate(textarea_fields, start=1):
            css_selector = self.get_css_path(field)
            
            # 필드별 상태 설정
            if css_selector in control_size_dict and control_size_dict[css_selector]['diagonal'] <= MIN_DIAGONAL_MM:
                diagonal = control_size_dict[css_selector]['diagonal']
                scanDTO = DTO.ScanDTO(
                    errortype=f"10.조작 가능(width:{window_size["width"]}px, height:{window_size["height"]}px)",
                    errormessage=textwrap.dedent(
                        f"""컨트롤의 크기는 대각선 길이가 6mm 이상이 되도록 제공해야 합니다. (현재 {round(diagonal*PIXEL_TO_MM, 2)}mm)"""
                    ),
                    erroroption="ERROR"
                )
                itemDTO = DTO.ItemDTO(
                    body=field.prettify(),
                    css_selector=css_selector,
                )
                if(css_selector in control_img_dict and control_img_dict[css_selector]['color_img_path']):
                    color_img_res = Api.post_create_img_item(control_img_dict[css_selector]['color_img_path'])
                    gray_img_res = Api.post_create_img_item(control_img_dict[css_selector]['gray_img_path'])
                    itemDTO = DTO.ItemDTO(
                        body=field.prettify(),
                        css_selector=css_selector,
                        colorimg=color_img_res['name'],
                        grayimg=gray_img_res['name']
                    )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        # 각 입력 필드에 대해 검사
        for index, field in enumerate(button_fields, start=1):
            css_selector = self.get_css_path(field)
            
            # 필드별 상태 설정
            if css_selector in control_size_dict and control_size_dict[css_selector]['diagonal'] <= MIN_DIAGONAL_MM:
                diagonal = control_size_dict[css_selector]['diagonal']
                scanDTO = DTO.ScanDTO(
                    errortype=f"10.조작 가능(width:{window_size["width"]}px, height:{window_size["height"]}px)",
                    errormessage=textwrap.dedent(
                        f"""컨트롤의 크기는 대각선 길이가 6mm 이상이 되도록 제공해야 합니다. (현재 {round(diagonal*PIXEL_TO_MM, 2)}mm)"""
                    ),
                    erroroption="ERROR"
                )
                itemDTO = DTO.ItemDTO(
                    body=field.prettify(),
                    css_selector=css_selector,
                )
                if(css_selector in control_img_dict and control_img_dict[css_selector]['color_img_path']):
                    color_img_res = Api.post_create_img_item(control_img_dict[css_selector]['color_img_path'])
                    gray_img_res = Api.post_create_img_item(control_img_dict[css_selector]['gray_img_path'])
                    itemDTO = DTO.ItemDTO(
                        body=field.prettify(),
                        css_selector=css_selector,
                        colorimg=color_img_res['name'],
                        grayimg=gray_img_res['name']
                    )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        for error_item in error_message:
            create_item = Api.post_create_item(request_id, error_item["item"])
            create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
        return error_message
    
    # 12.정지 기능 제공
    # 자동으로 변경되는 콘텐츠 추적
    def check_auto_changed_contents(self,
                                    request_id,
                                    auto_changed_image_list):
        error_message = []
        for auto_changed_image in auto_changed_image_list:
            scanDTO = DTO.ScanDTO(
                errortype="12.정지 기능 제공",
                errormessage=textwrap.dedent(
                    """자동으로 변경되는 콘텐츠를 확인하였습니다. 이전, 다음, 정지 기능을 제공하는지 확인하시오."""
                ),
                erroroption="WARNING"
            )
            img_res = Api.post_create_img_item(auto_changed_image)
            itemDTO = DTO.ItemDTO(
                body="",
                css_selector="",
                grayimg=img_res['name'],
                colorimg=img_res['name']
            )
            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        for error_item in error_message:
            create_item = Api.post_create_item(request_id, error_item["item"])
            create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
        return error_message
        


    # 14.반복 영역 건너뛰기
    # 14-1.반복되는 영역이 있는 경우, a태그를 활용한 건너뛰기 링크가 마크업상 최 상단에 위치해야 합니다.
    # 14-2.반복 영역 건너뛰기 기능은 키보드 접근 시 화면에 노출되어야 합니다.
    # 14-3.건너뛰기 대상으로 명시된 태그가 실제로 존재해야 합니다.
    def check_skip_link(self, 
                        request_id,
                        tab_selector_dict, 
                        tab_hidden_dict,
                        window_size):
        error_message = []
        header_tag = self.soup.find('header')
        header_id_tag = self.soup.select('#header')
        # 헤더 태그가 없으면 리턴
        if(not header_tag or not header_id_tag or not tab_selector_dict):
            return error_message
        
        # dict의 value를 기준으로 key를 정렬
        sorted_tab_select = sorted(tab_selector_dict, key=lambda x: tab_selector_dict[x])
        first_tab_select = sorted_tab_select[0]

        first_tab_tag = self.soup.select_one(first_tab_select)
        href_attribute = first_tab_tag.get('href')
        
        is_a_tag = first_tab_tag.name == "a"
        is_skip_link = href_attribute and href_attribute[0] == "#"
        is_first_tab_hidden = first_tab_tag in tab_hidden_dict
        
        # 14-1.반복되는 영역이 있는 경우, a태그를 활용한 건너뛰기 링크가 마크업상 최상단에 위치해야 합니다.
        if(not is_a_tag or not is_skip_link):
            scanDTO = DTO.ScanDTO(
                errortype=f"14.반복 영역 건너뛰기(width:{window_size["width"]}px, height:{window_size["height"]}px)",
                errormessage="반복되는 영역이 있는 경우, a태그를 활용한 건너뛰기 링크가 마크업상 최상단에 위치해야 합니다.",
                erroroption="ERROR"
            )
            itemDTO = DTO.ItemDTO(
                body=header_tag.prettify(),
                css_selector="header"
            )
            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        # 14-2.반복 영역 건너뛰기 기능은 키보드 접근 시 화면에 노출되어야 합니다
        if(is_skip_link and is_first_tab_hidden):
            scanDTO = DTO.ScanDTO(
                errortype=f"14.반복 영역 건너뛰기(width:{window_size["width"]}px, height:{window_size["height"]}px)",
                errormessage="반복 영역 건너뛰기 기능은 키보드 접근 시 화면에 노출되어야 합니다.",
                erroroption="ERROR"
            )
            itemDTO = DTO.ItemDTO(
                body=first_tab_tag.prettify(),
                css_selector=first_tab_select
            )
            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        
        # 14-3.건너뛰기 대상으로 명시된 태그가 실제로 존재해야 합니다.
        if(is_skip_link and not self.soup.select_one(href_attribute)):
            scanDTO = DTO.ScanDTO(
                errortype=f"14.반복 영역 건너뛰기(width:{window_size["width"]}px, height:{window_size["height"]}px)",
                errormessage="건너뛰기 대상으로 명시된 태그가 실제로 존재해야 합니다.",
                erroroption="ERROR"
            )
            itemDTO = DTO.ItemDTO(
                body=first_tab_tag.prettify(),
                css_selector=first_tab_select
            )
            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        for error_item in error_message:
            create_item = Api.post_create_item(request_id, error_item["item"])
            create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
        return error_message
    
    # 15.제목 제공
    def check_title(self,
                    request_id):
        error_message = []
        
        html_tag = self.soup.find('html')
        head_tag = self.soup.find('head')
        title_tag = self.soup.find('title')
        
        # 15-1. title 태그 찾기
        if not head_tag or not title_tag:
            scanDTO = DTO.ScanDTO(
                errortype="15.제목 제공",
                errormessage="<head> 태그에 페이지 내용을 유추할 수 있는 적절한 <title>을 제공해야 한다.",
                erroroption="ERROR"
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
                    errormessage="<iframe>에 적절한 title 속성을 제공해야 한다.",
                    erroroption="ERROR"
                )
                itemDTO = DTO.ItemDTO(
                    body=iframe.prettify(),
                    css_selector = self.get_css_path(iframe)
                )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        for error_item in error_message:
            create_item = Api.post_create_item(request_id, error_item["item"])
            create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
        return error_message
    
    # 16.적절한 링크 텍스트
    def check_link_text(self,
                        request_id):
        error_message = []
        a_list = self.soup.find_all('a')
        for i, a_tag in enumerate(a_list):
            a_innerHTML = a_tag.contents
            if not a_innerHTML:
                scanDTO = DTO.ScanDTO(
                    errortype="16.적절한 링크 텍스트",
                    errormessage="내부가 비어있는 <a> 태그는 제거하거나 수정해야 한다.",
                    erroroption="ERROR"
                )
                itemDTO = DTO.ItemDTO(
                    body=a_tag.prettify(),
                    css_selector = self.get_css_path(a_tag)
                )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        for error_item in error_message:
            create_item = Api.post_create_item(request_id, error_item["item"])
            create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
        return error_message
    
    # 17.기본 언어 표시
    def check_html_lang(self,
                        request_id):
        error_message = []
        tag_name = 'html'
        html_tag = self.soup.find(tag_name)
        if not html_tag.get('lang'):
            scanDTO = DTO.ScanDTO(
                errortype="17.기본 언어 표시",
                errormessage="<html> 태그에 주로 사용하는 언어를 lang 속성으로 명시해야 한다.",
                erroroption="ERROR"
            )
            itemDTO = DTO.ItemDTO(
                body=html_tag.prettify(),
                css_selector="html"
            )
            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        for error_item in error_message:
            create_item = Api.post_create_item(request_id, error_item["item"])
            create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
        return error_message
    
    # 18.사용자 요구에 따른 실행
    # 18-1.새 창이라는 것을 알 수 있도록 제공해야 한다.
    def check_new_window_onclick(self, 
                                 request_id):
        error_message = []
        a_list = self.soup.find_all('a')
        for i, a_tag in enumerate(a_list):
            a_target = a_tag.get('target')
            a_title = a_tag.get('title')
            a_onclick = a_tag.get('onclick')
            if a_target == "_blank" and not a_title:
                scanDTO = DTO.ScanDTO(
                    errortype="18.사용자 요구에 따른 실행",
                    errormessage="새 창이라는 것을 알 수 있도록 a 태그에 title을 제공해야 한다.",
                    erroroption="ERROR"
                )
                itemDTO = DTO.ItemDTO(
                    body=a_tag.prettify(),
                    css_selector = self.get_css_path(a_tag)
                )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
            elif a_onclick and "window.open" in a_onclick:
                scanDTO = DTO.ScanDTO(
                    errortype="18.사용자 요구에 따른 실행",
                    errormessage="새 창이라는 것을 알 수 있도록 a 태그에 title을 제공해야 한다.",
                    erroroption="ERROR"
                )
                itemDTO = DTO.ItemDTO(
                    body=a_tag.prettify(),
                    css_selector = self.get_css_path(a_tag)
                )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        for error_item in error_message:
            create_item = Api.post_create_item(request_id, error_item["item"])
            create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
        return error_message
    
    # 20.표의 구성
    # 20-1.표에 <caption>, summary 등을 사용하여 적절한 제목과 요약 정보를 제공한다.
    def check_table_head(self, 
                         request_id):
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
                    ),
                    erroroption="ERROR"
                )
                itemDTO = DTO.ItemDTO(
                    body=table.prettify(),
                    css_selector = self.get_css_path(table)
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
                    ),
                    erroroption="ERROR"
                )
                itemDTO = DTO.ItemDTO(
                    body=table.prettify(),
                    css_selector = self.get_css_path(table)
                )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        for error_item in error_message:
            create_item = Api.post_create_item(request_id, error_item["item"])
            create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
        return error_message
    
    # 21.레이블 제공
    def check_input_label(self, 
                          request_id):
        # 결과 저장용 리스트
        error_message = []
        
        # 검사 대상 입력 필드
        input_fields = self.soup.find_all(['input'], 
                             {'type': lambda x: x not in ['hidden', 'submit', 'reset', 'button', 'image']})
        textarea_fields = self.soup.find_all(['textarea'])
        select_fields = self.soup.find_all(['select'])

        # 각 입력 필드에 대해 검사
        for index, field in enumerate(input_fields, start=1):
            field_id = field.get('id', None)
            title_attr = field.get('title', None)
            label = self.soup.find('label', {'for': field_id}) if field_id else None
            
            # 필드별 상태 설정
            if not label and not title_attr:
                scanDTO = DTO.ScanDTO(
                    errortype="21.레이블 제공",
                    errormessage=textwrap.dedent(
                        """해당 입력 서식에 <label>을 연결하거나, title 속성을 추가해야 합니다."""
                    ),
                    erroroption="ERROR"
                )
                itemDTO = DTO.ItemDTO(
                    body=field.prettify(),
                    css_selector = self.get_css_path(field)
                )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        # 각 입력 필드에 대해 검사
        for index, field in enumerate(textarea_fields, start=1):
            field_id = field.get('id', None)
            title_attr = field.get('title', None)
            label = self.soup.find('label', {'for': field_id}) if field_id else None
            
            # 필드별 상태 설정
            if not label and not title_attr:
                scanDTO = DTO.ScanDTO(
                    errortype="21.레이블 제공",
                    errormessage=textwrap.dedent(
                        """해당 입력 서식에 <label>을 연결하거나, title 속성을 추가해야 합니다."""
                    ),
                    erroroption="ERROR"
                )
                itemDTO = DTO.ItemDTO(
                    body=field.prettify(),
                    css_selector = self.get_css_path(field)
                )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        # 각 입력 필드에 대해 검사
        for index, field in enumerate(select_fields, start=1):
            field_id = field.get('id', None)
            title_attr = field.get('title', None)
            label = self.soup.find('label', {'for': field_id}) if field_id else None
            
            # 필드별 상태 설정
            if not label and not title_attr:
                scanDTO = DTO.ScanDTO(
                    errortype="21.레이블 제공",
                    errormessage=textwrap.dedent(
                        """해당 입력 서식에 <label>을 연결하거나, title 속성을 추가해야 합니다."""
                    ),
                    erroroption="ERROR"
                )
                itemDTO = DTO.ItemDTO(
                    body=field.prettify(),
                    css_selector = self.get_css_path(field)
                )
                error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
        for error_item in error_message:
            create_item = Api.post_create_item(request_id, error_item["item"])
            create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
        return error_message
    
    # 23.마크업 오류 방지
    def check_w3c_markup(self, 
                         request_id):
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
                                errormessage=item['errormessage'],
                                erroroption="ERROR"
                            )
                            itemDTO = DTO.ItemDTO(
                                body=msg['extract'],
                                css_selector=f"From line {msg['lastLine']+1}, column {msg['firstColumn']}; to line {msg['lastLine']+1}, column {msg['lastColumn']}"
                            )
                            error_message.append({"scan" : dict(scanDTO), "item" : dict(itemDTO)})
            for error_item in error_message:
                create_item = Api.post_create_item(request_id, error_item["item"])
                create_scan = Api.post_create_scan(request_id, create_item["id"], error_item["scan"])
            return error_message
        return None
    
    def get_css_path(self, element):
        """Generate CSS path of a BeautifulSoup element, excluding [document]."""
        path = []
        while element and element.name != "[document]":
            # 태그 이름 가져오기
            selector = element.name

            # 형제 중 같은 태그가 있는 경우 nth-of-type으로 구분
            if element.parent:
                siblings = element.find_previous_siblings(element.name)
                if siblings:
                    index = len(siblings) + 1
                    selector += f":nth-of-type({index})"
            
            path.insert(0, selector)
            element = element.parent

        return " > ".join(path)
    
    def extract_tag_head(self, name : str ,tag : Tag):
        taghead = f"<{name}"
        for attr, value in tag.attrs.items():
            taghead += (f' {attr}="{value}"')
        taghead += ">"
        return taghead