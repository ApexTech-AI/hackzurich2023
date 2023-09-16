
import requests
import flask
from flask_cors import CORS
from flask import request, jsonify, for_url
from index_knowledge_base import index_knowledge_base, delete_index
from search import search_pdf_text
from common import vertexai


app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
URL_BASE = "http://localhost:5000/api/v1"


@app.route('/api/v1/autosearch', methods=['GET'])
def autosearch():
    question = request.args.get('question')

    keywords_url = url_for("generate_keywords")
    keywords_response = requests.post(URL_BASE+keywords_url, json={"prompt": question})
    keywords = keywords_response.json()['keywords']

    files_url = url_for("search", **{"keyword": kw for kw in keywords})
    files = requests.get(URL_BASE+files_url)

    result = files.json()['results']
    sleek_result = [x['id'] for x in result]

    return jsonify({'results': sleek_result})


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
        text = json['text']
    except KeyError as err:
        return jsonify({'error': 'Key text is missing'}), 400 

    result = vertexai.summarize_document(text)
    return jsonify({'summary': result})


@app.route('/api/v1/generate-keywords', methods=['POST'])
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

    return jsonify({'keywords': result_list})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)