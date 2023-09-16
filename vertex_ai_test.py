import vertexai
from vertexai.preview.language_models import TextGenerationModel
import PyPDF2

import requests
import json


# Open the PDF file
with open('./dataset/safety_data_sheet/BC-Bitumen-Coating-SDS-en_MY.pdf', 'rb') as f:
    # Create a PDF Reader object
    pdf_reader = PyPDF2.PdfReader(f)
    
    # Initialize an empty string to hold the PDF content
    pdf_text = ""
    
    # Loop through each page
    for i in range(len(pdf_reader.pages)):
        # Get a page object
        page = pdf_reader.pages[i]
        
        # Extract text from the page
        pdf_text += page.extract_text()
        
prompt = f'Analyse the following text and write a summary:\n{pdf_text}\nSummary:'
print(prompt)


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