from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_iris import IRISVectorStore
from flask import request, jsonify
import tempfile
import os

from llama_index.core import Settings
from utils import set_embedding_model, set_api_key

def similarity_engine_llama():
    request_data = request.get_json()
    if not request_data:
        return jsonify({"error": "No JSON data provided"}), 400

    # Get database details and collection name from JSON input
    username = request_data.get("username")
    password = request_data.get("password")
    hostname = request_data.get("hostname")
    port = request_data.get("port")
    namespace = request_data.get("namespace")
    table_name = request_data.get("table_name")
    indexing_type = request_data.get('indexing_type')
    model_name = request_data.get('model_name')
    embedding_dimension = request_data.get("embedding_dimension")
    score_cutoff = request_data.get("score_cutoff")
    results_count = request_data.get("results_count")
    query = request_data.get("query")

    api_key = request.headers.get("api-key")

    if not all([username, password, hostname, port, namespace, table_name, indexing_type, model_name, embedding_dimension, query, api_key]):
        return jsonify({"error": "Missing required parameters"}), 400

    CONNECTION_STRING = f"iris://{username}:{password}@{hostname}:{port}/{namespace}"

    set_api_key(indexing_type, api_key)

    vector_store = IRISVectorStore(
        connection_string=CONNECTION_STRING,
        table_name=table_name,
        schema_name='SQLUser',
        perform_setup= False,
        embed_dim= embedding_dimension
    )

    Settings.embed_model = set_embedding_model(indexing_type, model_name, api_key)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    top_k = 5
    if results_count:
        top_k = results_count
        
    retriever = index.as_retriever(similarity_top_k=top_k)

    nodes = retriever.retrieve(query)

    similarity_cutoff = 0
    if score_cutoff:
        similarity_cutoff = score_cutoff

    filtered_nodes = [node for node in nodes if node.score >= similarity_cutoff]

    result_list = []
    for node in filtered_nodes:
        result_list.append({
            "node_id": node.node_id,
            "similarity": node.score,
            "text": node.text
        })

    return jsonify({"result" : result_list})
