from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

import os
from llama_index.readers.base import BaseReader
#from llama_index import download_loader, GPTVectorStoreIndex
import pickle
from llama_index.readers.github_readers.github_repository_reader import GithubRepositoryReader
from llama_index.readers.github_readers.github_api_client import (
    GitBranchResponseModel,
    GitCommitResponseModel,
    GithubClient,
    GitTreeResponseModel,
)
from llama_index import SimpleDirectoryReader, ServiceContext, LLMPredictor
from llama_index.node_parser import SimpleNodeParser
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index.storage.storage_context import StorageContext
from llama_index import SimpleDirectoryReader, ServiceContext, LLMPredictor
from llama_index import GPTVectorStoreIndex, GPTListIndex, GPTSimpleKeywordTableIndex
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveChararacterTextSplitter

from load_env_var import GITHUB_TOKEN, OPENAI_API_KEY

def git_repo_reader(repo_owner, repo_url):
    """Read a git repository"""
    reader = GithubRepositoryReader(
        owner = repo_owner,
        repo=repo_url,
        verbose=True,
        github_token=GITHUB_TOKEN,
        ignore_directories=[".git", ".github", "docs", "tests", "examples", "node_modules", "dist"],
    )
    documents = reader.load_data(branch="main")
    return documents

def load_docs(repo_url):
    """Load documents from a repository"""
    reader = SimpleDirectoryReader(repo_url)
    documents = reader.load_data()

    return documents


def chunk_data_into_smaller_docs(documents):
    """Chunk data into smaller documents"""
    text_splitter = RecursiveChararacterTextSplitter(chunk_size=1024, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    print("Number of texts: ", len(texts))
    return texts


def parse_into_nodes(documents):
    """Parse documents into nodes"""
    nodes = SimpleNodeParser().get_nodes_from_documents(documents)
    return nodes

def add_to_docsstore(nodes):
    """Add nodes to docsstore"""
    docstore = SimpleDocumentStore()
    docstore.add_documents(nodes)
    return docstore

def define_multiple_indexes(nodes, docstore):
    """Define multiple indexes"""
    storage_context = StorageContext.from_defaults(docstore=docstore)
    list_index = GPTListIndex(nodes, storage_context=storage_context)
    vector_index = GPTVectorStoreIndex(nodes, storage_context=storage_context) 
    keyword_table_index = GPTSimpleKeywordTableIndex(nodes, storage_context=storage_context) 
    len(storage_context.docstore.docs)
    
    return (list_index, vector_index, keyword_table_index)

def test_some_queries(list_index, vector_index, keyword_table_index):
    """Test some queries"""
    llm_predictor_chatgpt = LLMPredictor(llm=ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0, model_name="gpt-3.5-turbo"))
    service_context_chatgpt = ServiceContext.from_defaults(llm_predictor=llm_predictor_chatgpt, chunk_size_limit=1024)
    query_engine = list_index.as_query_engine()

    while (True):
        input_test = input("Enter question: ")

        response = query_engine.query(input_test) 
        print(response)
