import PyPDF2
import os
from common import PDF_INDEX, elasticsearch as es


def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text()
        return text
    except PyPDF2.errors.PdfReadError as e:
        print(f"An error occured while processing '{pdf_path}': {str(e)}")


def index_pdf_text(pdf_text, doc_id):
    es.index(index="pdf_index", id=doc_id, body={'text': pdf_text})


def index_pdf(pdf_path):
    text = extract_text_from_pdf(pdf_path)
    index_pdf_text(text, pdf_path)


def index_knowledge_base(base_path=os.path.join('.', 'dataset')):
    folder_total = len(list(os.walk(base_path)))
    for i, (root, dirs, files) in enumerate(os.walk(base_path)):
        print(f'Indexing folder {1+i} out of {folder_total}')
        for j, filename in enumerate(files):
            print(f'\tIndexing file {1+j} out of {len(files)} - {round(100 * (i + j / len(files)) / folder_total, 2)}%')
            file_path = os.path.join(root, filename)
            _, file_extension = os.path.splitext(file_path)
            if file_extension == '.pdf':
                index_pdf(file_path)


def delete_index():
    if es.indices.exists(index=PDF_INDEX):
        es.indices.delete(index=PDF_INDEX)
        print(f'Successfully deleted index {PDF_INDEX}')
    else:
        print(f'Index {PDF_INDEX} does not exist')


if __name__ == '__main__':    
    index_knowledge_base()