from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.postprocessor.cohere_rerank import CohereRerank
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.llms.openai import OpenAI
from llama_index.core import QueryBundle
from llama_index.postprocessor.rankgpt_rerank import RankGPTRerank
from llama_iris import IRISVectorStore
from flask import request, jsonify
import tempfile
import os

from llama_index.core import Settings
from utils import set_embedding_model, set_api_key

def reco_engine_llama():
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
    reco_type = request_data.get("reco_type")
    results_count = request_data.get("results_count")
    query = request_data.get("query")

    api_key = request.headers.get("api-key")
    cohere_api_key = request.headers.get("cohere-api-key")
    openai_api_key = request.headers.get("openai-api-key")

    if not all([username, password, hostname, port, namespace, table_name, indexing_type, model_name, embedding_dimension, reco_type, results_count, query, api_key]):
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

    if reco_type == 'cohere_rerank':
        cohere_rerank = CohereRerank(api_key=cohere_api_key, top_n=results_count)
        query_engine = index.as_query_engine(
            similarity_top_k=10,
            node_postprocessors=[cohere_rerank],
        )
        response = query_engine.query(query)

        result_list = []
        for node in response.source_nodes:
            result_list.append({
                "node_id": node.node_id,
                "similarity": node.score,
                "text": node.text
            })
    
    elif reco_type == 'openai_rerank':
        rankgpt_rerank = RankGPTRerank(
            llm=OpenAI(
                model="gpt-3.5-turbo-16k",
                temperature=0.0,
                api_key=openai_api_key,
            ),
            top_n=results_count,
            verbose=True,
        )
        query_engine = index.as_query_engine(
            similarity_top_k=10,
            node_postprocessors=[rankgpt_rerank],
        )
        response = query_engine.query(query)

        result_list = []
        for node in response.source_nodes:
            result_list.append({
                "node_id": node.node_id,
                "similarity": node.score,
                "text": node.text
            })
    
    return jsonify({"response" : str(response), "source": result_list})
    query_bundle = QueryBundle(query_str)
    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=vector_top_k,
    )
    retrieved_nodes = retriever.retrieve(query_bundle)

    reranker = RankGPTRerank(
        llm=OpenAI(
            model="gpt-3.5-turbo-16k",
            temperature=0.0,
            api_key=openai_api_key,
        ),
        top_n=reranker_top_n,
        verbose=True,
    )
    retrieved_nodes = reranker.postprocess_nodes(
        retrieved_nodes, query_bundle
    )

    return retrieved_nodes