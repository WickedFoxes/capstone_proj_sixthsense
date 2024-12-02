class ItemDTO:
    def __init__(self, 
            body : str,
            css_selector : str = "",
            colorimg : str = "",
            grayimg : str = "",
            itemtype : str = "TEXT",
            tabindex : int = -1
    ):
        self.body = body
        self.css_selector = css_selector
        self.colorimg = colorimg
        self.grayimg = grayimg
        self.itemtype = itemtype
        self.tabindex = tabindex
    def __iter__(self):
        yield 'body', self.body
        yield 'css_selector', self.css_selector
        yield 'colorimg', self.colorimg
        yield 'grayimg', self.grayimg
        yield 'itemtype', self.itemtype
        yield 'tabindex', self.tabindex

class ScanDTO:
    def __init__(self, 
            errortype : str,
            errormessage : str,
            guide : str = "",
            erroroption : str = "ERROR"
        ):
        self.errortype = errortype
        self.errormessage = errormessage
        self.guide = guide
        self.erroroption = erroroption
    def __iter__(self):
        yield 'errortype', self.errortype
        yield 'errormessage', self.errormessage
        yield 'guide', self.guide
        yield 'erroroption', self.erroroption