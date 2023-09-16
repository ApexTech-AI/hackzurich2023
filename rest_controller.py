from flask import Flask, request, jsonify
from index_knowledge_base import index_knowledge_base, delete_index
from search import search_pdf_text
from common import vertexai
import json

app = Flask(__name__)


@app.route('/search', methods=['GET'])
def search():
    keywords = request.args.getlist('keyword')

    if keywords is None:
        return jsonify({'error': 'Query parameter is missing'}), 400

    results = search_pdf_text(keywords)
    return jsonify({'results': results})


@app.route('/reseed', methods=['POST'])
def reseed_database():
    delete_index()
    index_knowledge_base()
    return jsonify({'message': 'Reseed operation completed'})


@app.route('/summarize', methods=['POST'])
def summarize_pdf():
    json = request.get_json()

    if json is None:
        return jsonify({'error': 'JSON File is missing'}), 400 

    try:
        text = json['text']
    except KeyError as err:
        return jsonify({'error': 'Key text is missing'}), 400 

    result = vertexai.summarize_document(text)
    return jsonify({'summary': result})


@app.route('/generate-keywords', methods=['POST'])
def generate_keywords():
    json_file = request.get_json()

    if json_file is None:
        return jsonify({'error': 'JSON File is missing'}), 400 

    try:
        prompt = json_file['prompt']
    except KeyError as err:
        return jsonify({'error': 'Key prompt is missing'}), 400 

    result = vertexai.get_keywords(prompt)

    result_list = result.split(': ')[1].split(', ')

    return "{\"keywords\":" + str(result_list) + "}", 200


if __name__ == '__main__':
    app.run()
