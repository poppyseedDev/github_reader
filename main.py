from create_embeddings import create_embeddings, create_pinecone_index, test_pinecone
import streamlit as st
from streamlit_interface import StreamlitInterface
from process_gpt import chunk_data_into_smaller_docs

def main():
    """Main function"""
    documents = StreamlitInterface().start_interface()
    texts = chunk_data_into_smaller_docs(documents)
    
    embeddings = create_embeddings()
    create_pinecone_index(texts=texts, embeddings=embeddings)
    test_pinecone()
