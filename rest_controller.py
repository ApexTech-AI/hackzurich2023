from flask import Flask, request, jsonify
from index_knowledge_base import index_knowledge_base, delete_index
from search import search_pdf_text
from common import vertexai
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})


@app.route('/api/v1/search', methods=['POST'])
def search():
<<<<<<< Updated upstream
    keywords = request.args.getlist('keyword')

    if keywords is None:
        return jsonify({'error': 'Query parameter is missing'}), 400

    results = search_pdf_text(keywords)
    return jsonify({'results': results})
=======
    
    keywords = request.get_json()['keywords']

    if keywords is None or len(keywords) == 0:
        return jsonify({'error': 'Query parameter is missing'}), 400

    # Init empty set
    result_docs = {}
    for k in keywords:
        results = search_pdf_text(keyword)
        for doc in results
            result_docs.add(doc)
        
    
    return jsonify({'results': str(list(results))})
>>>>>>> Stashed changes


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

    return "{\"keywords\":" + str(result_list) + "}", 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)