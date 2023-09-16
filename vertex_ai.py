import vertexai
from vertexai.preview.language_models import TextGenerationModel
import PyPDF2

import requests
import json

class VertexAI():
    def __init__(self):
        pass


    def summarize_document(self, content):
        prompt = f'Analyse the following text and write a summary:\n{content}\nSummary:'
        print(prompt)
        execute_prompt(prompt)

        

    def get_keywords(self, search_phrase):
        prompt = f'You are responsible for managing a search engine of a company\'s knowledge base that is selling concrete and machinery to concrete. Users come to you with search phrases. Suggest new keywords to your user in a json format to following search terms:\n{search_phrase}. The suggestions shall be stored as a list of strings with the key \'suggestions\'.' 
        print(prompt)
        execute_prompt(prompt)

    def execute_prompt(self, prompt):
        vertexai.init(project="hackzurich23-8229", location="us-central1")
        parameters = {
            "max_output_tokens": 1024,
            "temperature": 0.2,
            "top_p": 0.8,
            "top_k": 40
        }
        model = TextGenerationModel.from_pretrained("text-bison-32k")
        response = model.predict(
            prompt,
            **parameters
        )
        print(f"Response from Model: {response.text}")


vAI = VertexAI()
vAI.get_keywords("What is the difference between a PU injection foam and PU injection resin?")