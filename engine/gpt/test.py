from gpt import TextGPT

gpt = TextGPT(prompt_path="prompt/test.prompt")
print(gpt.get("<a href=\"javascript:void(0)\" title=\"검색\" class=\"btn_topSearch\" >검색하기</a>"))