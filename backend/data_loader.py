import os
import tempfile
from flask import request, jsonify
from s3fs import S3FileSystem
from llama_index.core import (VectorStoreIndex,SimpleDirectoryReader,StorageContext)
from llama_index.core import Settings

from utils import set_embedding_model, set_api_key
from llama_iris import IRISVectorStore

def upload_data():
    username = request.form.get('username')
    password = request.form.get('password')
    hostname = request.form.get('hostname')
    port = request.form.get('port')
    namespace = request.form.get('namespace')
    table_name = request.form.get('table_name')
    load_type = request.form.get('load_type')
    indexing_type = request.form.get('indexing_type')
    model_name = request.form.get('model_name')
    embedding_dimension = request.form.get('embedding_dimension')

    api_key = request.headers.get("api-key")

    if not all([username, password, hostname, port, namespace, table_name, load_type, indexing_type, model_name, embedding_dimension, api_key]):
        return jsonify({"error": "Missing required parameters"}), 400

    set_api_key(indexing_type, api_key)

    if load_type == "local":
        # Check for uploaded files
        if "files" not in request.files:
            return jsonify({"error": "No files uploaded"}), 400

        uploaded_files = request.files.getlist("files")
        if len(uploaded_files) > 10:
            return jsonify({"error": "Exceeded maximum file limit (10)"}), 400

        temp_paths = []
        for uploaded_file in uploaded_files:
            fd, temp_path = tempfile.mkstemp()
            with os.fdopen(fd, "wb") as temp:
                uploaded_file.save(temp)
            temp_paths.append(temp_path)

        # Load data from files
        documents = SimpleDirectoryReader(input_files=temp_paths).load_data()

    elif load_type == "aws_s3":
        access_key = request.form.get('aws_access_key')
        secret = request.form.get('aws_secret')
        bucket_name = request.form.get('aws_bucket_name')

        if not all([access_key, secret, bucket_name]):
            return jsonify({"error": "Missing required AWS S3 parameters"}), 400

        s3_fs = S3FileSystem(key=access_key, secret=secret)
        reader = SimpleDirectoryReader(input_dir=bucket_name, fs=s3_fs, recursive=True)
        documents = reader.load_data()

    else:
        return jsonify({"error": "Invalid input type"}), 400

    CONNECTION_STRING = f"iris://{username}:{password}@{hostname}:{port}/{namespace}"

    vector_store = IRISVectorStore.from_params(
        connection_string=CONNECTION_STRING,
        table_name=table_name,
        embed_dim=embedding_dimension
    )

    Settings.embed_model = set_embedding_model(indexing_type, model_name, api_key)

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context
    )

    return jsonify({"message": "Documents uploaded successfully"})
