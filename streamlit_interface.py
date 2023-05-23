import streamlit as st
from process_gpt import git_repo_reader, load_docs, parse_into_nodes, add_to_docsstore, define_multiple_indexes, test_some_queries

def parse_git_url(git_url):
    """Parse a git URL into the owner and repo name"""
    (repo_owner, repo_name) = git_url.split("/")[-2:]
    return (repo_owner, repo_name)
    

def load_repo_from_github(git_url):
    """Load a repository from GitHub"""
    (repo_owner, repo_name) = parse_git_url(git_url)
    st.write(f"Loading the repository {repo_name}...")
    documents= git_repo_reader(repo_owner, repo_name)
    st.write("Repository loaded.")
    print(f'Number of documents: {len(documents)}')
    return documents