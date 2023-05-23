from create_embeddings import create_embeddings, create_pinecone_index, test_pinecone
import streamlit as st
from streamlit_interface import load_repo_from_github

def main():
    st.title("💻🦾 Load a GitHub repository")
    git_url = st.text_input("Enter the GitHub URL of the repository: ")

    if git_url:
        documents = load_repo_from_github(git_url)
        
        embeddings = create_embeddings()
        create_pinecone_index(embeddings=embeddings, )
        test_pinecone()
