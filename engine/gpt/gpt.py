from openai import OpenAI
from dotenv import load_dotenv
import os
import tiktoken
from pydantic import BaseModel
load_dotenv()

class OutputFormat(BaseModel):
    explain: str
    isNeedModify: str
    Modify: str

class TextGPT:
    def __init__(
            self,
            prompt_path : str,
            model : str = "gpt-4o-2024-08-06"
        ):
        OpenAI.api_key = os.environ.get('OPENAI_API_KEY')
        self.client = OpenAI()
        self.messages = []
        self.model = model
        self.prompt = self.readPrompt(prompt_path)

    def readPrompt(self, prompt_path):
        f = open(prompt_path, 'rb')
        return f.read().decode(encoding="utf-8")

    def get(self, user_message):
        response = self.client.beta.chat.completions.parse(
            model=self.model,
            messages=[
                {"role" : "system", "content" : self.prompt},
                {"role" : "user", "content" : user_message},
            ],
            response_format=OutputFormat,
        )
        return response.choices[0].message.parsed


class VisionGPT:
    def __init__(
            self,
            prompt_path : str,
            model : str = "gpt-4o"
        ):
        OpenAI.api_key = os.environ.get('OPENAI_API_KEY')
        self.client = OpenAI()
        self.messages = []
        self.model = model
        self.prompt = self.readPrompt(prompt_path)
        
    def readPrompt(self, prompt_path):
        f = open(prompt_path, 'rb')
        return f.read().decode(encoding="utf-8")

    def get(self, user_img):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{
                "role" : "user", 
                "content" : [
                    {"type": "text", "text": self.prompt},
                    {"type": "image_url", "image_url": {"url" : user_img}},
                ]
            }]
        )
        return response.choices[0].message.content
    
class Token:
    def __init__(
        self, 
        texts : str,
        model : str = "gpt-4o"
    ):
        self.texts = texts
        self.model = model

    def token_count(self):
        return len(self.tokenizer(self.model))
    
    def tokenizer(self):
        encoding = tiktoken.encoding_for_model(self.model)
        tokens = encoding.encode(self.texts)
        return tokens