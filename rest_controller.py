#!/usr/bin/env python3

import requests
import flask
from flask_cors import CORS
from flask import request, jsonify, url_for
from index_knowledge_base import index_knowledge_base, delete_index, extract_text_from_pdf
from search import search_pdf_text
from common import vertexai
from PyPDF2 import PdfReader
import os.path


app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
URL_BASE = "http://localhost:5000"

last_search = dict()

@app.route('/api/v1/autosearch', methods=['POST'])
def autosearch():
    json = request.get_json()

    if json is None:
        return jsonify({'error': 'JSON File is missing'}), 400 

    try:
        question = json['question']
    except KeyError as err:
        return jsonify({'error': 'Key question is missing'}), 400 

    keywords = get_keywords_list(question)

    files_url = url_for("search")
    files = requests.post(URL_BASE+files_url+"?"+'&'.join("keyword="+kw for kw in keywords))

    result = files.json()['results']

    sleek_result = set()
    for x in result:
        sleek_result.add(x['id'])

    return jsonify({'results': list(sleek_result)})


@app.route('/api/v1/search', methods=['POST'])
def search():
    keywords = request.args.getlist('keyword')

    if keywords is None:
        return jsonify({'error': 'Query parameter is missing'}), 400

    results = search_pdf_text(keywords)
    return jsonify({'results': results})


@app.route('/api/v1/reseed', methods=['POST'])
def reseed_database():
    delete_index()
    index_knowledge_base()
    return jsonify({'message': 'Reseed operation completed'})


@app.route('/api/v1/summarize', methods=['POST'])
def summarize_pdf():
    json = request.get_json()

    if json is None:
        return jsonify({'error': 'JSON File is missing'}), 400 

    try:
        path = json['path']
    except KeyError as err:
        return jsonify({'error': 'Key path is missing'}), 400 

    try:
        prompt = json['prompt']
    except KeyError as err:
        return jsonify({'error': 'Key prompt is missing'}), 400 

    if not os.path.exists(path):
        return jsonify({'error': 'File does not exist'}), 400

    # Retrieve PDF Metadata
    with open(path, 'rb') as f:
        pdf = PdfReader(f)
        info = pdf.metadata
        author = info.author
        title = info.title
        date = info.modification_date

    # if path in last_search.keys():
    #    return jsonify({'summary': last_search[path], 'author': author, 'title': title, 'date': date})

    text = extract_text_from_pdf(path)
    result = vertexai.summarize_document(prompt, text)
    # last_search[path] = result
    return jsonify({'summary': result, 'author': author, 'title': title, 'date': date})


@app.route('/api/v1/generate_keywords', methods=['POST'])
def generate_keywords():
    json_file = request.get_json()

    if json_file is None:
        return jsonify({'error': 'JSON File is missing'}), 400 

    try:
        prompt = json_file['prompt']
    except KeyError as err:
        return jsonify({'error': 'Key prompt is missing'}), 400 

    result_list = get_keywords_list(prompt)

    return jsonify({'keywords': result_list})


def get_keywords_list(prompt):
    print (f'This is our prompt {prompt}')
    result = vertexai.get_keywords(prompt)
    result_list = result.split(', ')
    return result_list


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)