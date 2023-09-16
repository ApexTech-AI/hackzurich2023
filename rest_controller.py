from flask import Flask, request, jsonify
from index_knowledge_base import index_knowledge_base, delete_index
from search import search_pdf_text

app = Flask(__name__)


@app.route('/search', methods=['GET'])
def search():
    keyword = request.args.get('keyword')

    if keyword is None:
        return jsonify({'error': 'Query parameter is missing'}), 400

    results = search_pdf_text(keyword)
    return jsonify({'results': results})


@app.route('/reseed', methods=['POST'])
def reseed_database():
    delete_index()
    index_knowledge_base()
    return jsonify({'message': 'Reseed operation completed'})


@app.route('/summarize', methods=['GET'])
def summarize_pdf():
    id = request.args.get('id')

    if id is None:
        return jsonify({'error': 'Parameter ID is missing'}), 400 

    return jsonify({'result': 'This is great'})

if __name__ == '__main__':
    app.run()
