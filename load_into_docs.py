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
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownTextSplitter, TextSplitter
from git import Repo
from langchain.document_loaders import GitLoader

from load_env_var import GITHUB_TOKEN, OPENAI_API_KEY

def git_repo_reader(repo_owner, repo_name):
    """Read a git repository"""
    reader = GithubRepositoryReader(
        owner = repo_owner,
        repo=repo_name,
        
        verbose=True,
        github_token=GITHUB_TOKEN,
        ignore_directories=[".git", ".github", "docs", "tests", "examples", "node_modules", "dist"],
    )
    documents = reader.load_data(branch="main")
    return documents

def clone_git_repo(git_url):
    """Clone a git repository"""
    repo_name = git_url.split("/")[-1]
    path_to_clone = "./repos/" + repo_name

    # check if repo exists
    if os.path.exists(path_to_clone):
        print("Repo already exists")
        return path_to_clone, "main"
    # clone repo if it doesn't exist
    else:
        repo = Repo.clone_from(
            git_url, to_path=path_to_clone
        )
        branch = repo.head.reference
        return path_to_clone, branch

def load_git_from_disk(path_of_repo, branch):
    """Load git from disk"""
    #loader = GitLoader(
    #    repo_path=path_of_repo, branch=branch)
    optional_filter = lambda file_path: file_path.endswith(".md")
    loader = GitLoader(
        repo_path=path_of_repo, 
        branch=branch,
        file_filter=lambda file_path: file_path.endswith(".md"))

    data = loader.load()
    return data

def load_docs(repo_url):
    """Load documents from a repository"""
    reader = SimpleDirectoryReader(repo_url)
    documents = reader.load_data()

    return documents

def chunk_data_into_smaller_docs(documents):
    """Chunk data into smaller documents"""
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    print("Number of texts: ", len(texts))
    return texts

def chunk_data_based_on_markdown(documents):
    """Chunk data based on markdown"""
    text_splitter = MarkdownTextSplitter(chunk_size=1024, chunk_overlap=0)
    text = text_splitter.split_documents(documents)
    print(text)
    return text
