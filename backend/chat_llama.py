from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_iris import IRISVectorStore
from flask import request, jsonify
import tempfile
import os

from llama_index.core import Settings

from utils import set_embedding_model, set_api_key

def chat_engine_llama():
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
    messages = request_data.get("messages")

    api_key = request.headers.get("api-key")

    if not all([username, password, hostname, port, namespace, table_name, indexing_type, model_name, embedding_dimension, messages]):
        return jsonify({"error": "Missing required parameters"}), 400
    
    set_api_key(indexing_type, api_key)

    # Get the latest message from the list of messages
    latest_message = messages[-1]

    # Get the text of the latest user message
    user_message = latest_message.get("text")

    if not user_message:
        return jsonify({"error": "No text in the latest message"}), 400

    CONNECTION_STRING = f"iris://{username}:{password}@{hostname}:{port}/{namespace}"

    vector_store = IRISVectorStore(
        connection_string=CONNECTION_STRING,
        table_name=table_name,
        schema_name='SQLUser',
        perform_setup= False,
        embed_dim= embedding_dimension,
        debug= True
    )

    Settings.embed_model = set_embedding_model(indexing_type, model_name, api_key)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    chat_engine = index.as_chat_engine(chat_mode='condense_question')
    response = chat_engine.chat(user_message)
    
    return jsonify({"text": str(response)})
