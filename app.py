import flask
from flask_cors import CORS
from flask import request, jsonify
from llm_interaction.llama_interaction import LlamaLMI
from llm_interaction.hf_interaction import HuggingfaceLMI
from search import SearchEngine

app = flask.Flask(__name__)
app.config["DEBUG"] = True
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
search_eng = SearchEngine()

@api.route('/getdata', methods=['GET'])
def get_data():
    # Maybe we need to get something?
    return jsonify({"data": data_storage})

@api.route('/postdata', methods=['POST'])
def post_data():
    new_data = request.json.get('new_data', None)
    #TODO: Implement search
    if new_data is None:
        return jsonify({"error": "No data provided"}), 400

    data_storage.append(new_data)
    return jsonify({"message": "Data added", "new_data": new_data})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)