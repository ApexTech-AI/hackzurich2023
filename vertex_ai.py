import vertexai
from vertexai.preview.language_models import TextGenerationModel
import PyPDF2

import requests
import json

class VertexAI():
    def __init__(self):        
        vertexai.init(project="hackzurich23-8229", location="us-central1")
        self.parameters = {
            "max_output_tokens": 1024,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        }
        self.model = TextGenerationModel.from_pretrained("text-bison")


    def summarize_document(self, prompt, content):
        prompt = f'Analyse the following question: \n{prompt} \nAnd write a short summary to the following text and put it in relation to the previous question. Text:\n{content}\nSummary:'
        return self.execute_prompt(prompt)        

    def get_keywords(self, search_phrase):
        prompt = f'Using this phrase: \n{search_phrase}\n Generate keywords as a comma-separated plain-text list from the phrase. Each new keyword shall either be a single or composed term. The suggestions shall be stored as a list of strings with the key \'suggestions\'.' 
        return self.execute_prompt(prompt)

    def execute_prompt(self, prompt):
        response = self.model.predict(
            prompt,
            **self.parameters
        )
        print (response.text)
        return response.text
