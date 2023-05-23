from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
import os
from load_env_var import OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_API_ENV

def create_embeddings():
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    return embeddings

def create_pinecone_index(texts, embeddings):
    """Create a Pinecone index"""
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_API_ENV
    )
    index_name = "test"
    docsearch = Pinecone.from_texts(
        [t for t in texts], 
        embeddings, 
        index_name=index_name
        )
    return docsearch

def test_pinecone(docsearch):
    """Test Pinecone"""
    query = "Of what does this repo consist of?"
    docs = docsearch.similarity_search(
        query=query,
        include_metadata=True,
    )
    print(docs)
    

