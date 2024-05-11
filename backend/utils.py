import os

from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.embeddings.cohere import CohereEmbedding

def set_api_key(indexing_type, api_key):
    if api_key:
        if indexing_type == 'openai_embeddings':
            os.environ['OPENAI_API_KEY'] = api_key
        elif indexing_type == 'cohere_embeddings':
            os.environ['COHERE_API_KEY'] = api_key
        else:
            print("Invalid Indexing Value")

def set_embedding_model(indexing_type, model_name, api_key):
    if model_name:
        if indexing_type == 'openai_embeddings':
            return OpenAIEmbedding(model_name=model_name, api_key=api_key)
        elif indexing_type == 'cohere_embeddings':
            return CohereEmbedding(model_name=model_name, input_type="search_document", cohere_api_key=api_key)
        else:
            print("Invalid Indexing Value")
