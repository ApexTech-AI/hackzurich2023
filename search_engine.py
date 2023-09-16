import PyPDF2
import os
from elasticsearch import Elasticsearch


INDEX_KNOWLEDGE_BASE = False
es = Elasticsearch()


def extract_text_from_pdf(pdf_path):
    try:
        text = ""
        with open(pdf_path, 'rb') as pdf_file:
            pdf_reader = PyPDF2.PdfFileReader(pdf_file)
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text += page.extractText()
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


def search_pdf_text(keyword):
    search_result = es.search(index='pdf_index', body={'query': {'match': {'text': keyword}}})
    hits = search_result.get('hits', {}).get('hits', [])
    if not hits:
        print(f"No hits on query {keyword}")
        return []
    for hit in hits:
        print(hit.get("_id", "Error: Malformatted response"))
    return list(map(lambda x: {"id": hit.get("_id"), "text": hit.get("_source").get("text")}, hits))


if INDEX_KNOWLEDGE_BASE:
    index_knowledge_base()