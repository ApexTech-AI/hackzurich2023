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

    def sanity_check(self, summary, init_prompt):
        prompt = f'Your task is to judge with YES or NO if a given summary is answering a given prompt. Instance:\nPROMPT: What is C++?\nSUMMARY: C++ is a programming language.\nANSWER: Yes, the summary answers the prompt.\nInstance:\nPROMPT: Why is the earth round?\nSUMMARY: Cats are very fury, unlike most humans.\nANSWER: No, the summary doesn\'t answer the prompt. Your task:\nPROMPT:{init_prompt}\nSUMMARY:{summary}\nANSWER:'
        response = self.execute_prompt(prompt)
        if "yes" in response.lower():
            return True
        else:
            return False
        
    def answer_question(self, init_prompt):
        prompt = f'You are a helpful chatbot trying to answer the question to the best of your knowledge. You will get a single prompt and you will need to answer the question as short as possible. It is forbidden to pose further questions. There can be only one question and one short answer:\nQUESTION: {init_prompt}\nANSWER:'
        return self.execute_prompt(prompt)
    
    def summarize_document(self, user_prompt, content):
        prompt = f'Analyse the following question:\n{user_prompt}\nAnd write a short summary to the following text and put it in relation to the previous question. Text:\n{content}\nSummary:'
        summary = self.execute_prompt(prompt)
        is_an_answer = self.sanity_check(summary, user_prompt)
        if is_an_answer:
            print("valid summary")
            return summary, True
        else:
            print("invalid summary")
            return self.answer_question(user_prompt), False

    def get_keywords(self, phrase):
        prompt = f'Generate related keywords from the phrase:\n{phrase}\nEach keyword shall either be a single term or composed terms.\nDeliver the keywords as a comma-separated list of strings.' 
        return self.execute_prompt(prompt)

    def execute_prompt(self, prompt):
        response = self.model.predict(
            prompt,
            **self.parameters
        )
        print(response.text)
        return response.text
