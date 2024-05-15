# app.py
from flask import Flask, request, jsonify
from database import query_database
from query_llama import query_engine_llama
from chat_llama import chat_engine_llama
from similarity_llama import similarity_engine_llama
from reco_llama import reco_engine_llama
from data_loader import upload_data
from list_tables import get_table_list

app = Flask(__name__)

@app.route('/query', methods=['POST'])
def query_route():
    request_data = request.get_json()
    username = request_data.get('username')
    password = request_data.get('password')
    hostname = request_data.get('hostname')
    port = request_data.get('port')
    namespace = request_data.get('namespace')
    query = request_data.get('query')
    return jsonify(query_database(username, password, hostname, port, namespace, query))

@app.route("/query_engine", methods=["POST"])
def query_engine_route():
    return query_engine_llama()

@app.route("/chat_engine", methods=["POST"])
def chat_engine_route():
    return chat_engine_llama()

@app.route("/similarity_engine", methods=["POST"])
def similarity_engine_route():
    return similarity_engine_llama()

@app.route("/reco_engine", methods=["POST"])
def reco_engine_route():
    return reco_engine_llama()

@app.route("/upload_data", methods=["POST"])
def upload_data_route():
    return upload_data()

@app.route('/tables')
def tables():
    return get_table_list(request)

if __name__ == '__main__':
    app.run(debug=True)
