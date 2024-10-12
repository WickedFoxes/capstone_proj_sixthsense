class ItemDTO:
    def __init__(self, 
            body : str,
            colorimg : str = "",
            grayimg : str = "",
            itemtype : str = "TEXT",
            tabindex : int = 0
        ):
        self.body = body
        self.colorimg = colorimg
        self.grayimg = grayimg
        self.itemtype = itemtype
        self.tabindex = tabindex
    def __iter__(self):
        yield 'body', self.body
        yield 'colorimg', self.colorimg
        yield 'grayimg', self.grayimg
        yield 'itemtype', self.itemtype
        yield 'tabindex', self.tabindex

class ScanDTO:
    def __init__(self, 
            errortype : str,
            errormessage : str,
            guide : str = "",
        ):
        self.errortype = errortype
        self.errormessage = errormessage
        self.guide = guide
    def __iter__(self):
        yield 'errortype', self.errortype
        yield 'errormessage', self.errormessage
        yield 'guide', self.guide