import streamlit as st
from process_gpt import git_repo_reader, load_docs, parse_into_nodes, add_to_docsstore, define_multiple_indexes, test_some_queries
from process_gpt import chunk_data_into_smaller_docs
from create_embeddings import create_embeddings, create_pinecone_index, test_pinecone

class StreamlitInterface:
    def __init__(self):
        self.repo_owner = None
        self.repo_name = None
        
    def start_interface(self):
        st.title("💻🦾 Load a GitHub repository")
        git_url = st.text_input("Enter the GitHub URL of the repository: ")
        if git_url:
            # Parse the git URL
            self.parse_git_url(git_url=git_url)

            documents = self.load_repo_from_github()
            texts = chunk_data_into_smaller_docs(documents)
    
            embeddings = create_embeddings()
            create_pinecone_index(texts=texts, embeddings=embeddings)
            test_pinecone()

    def parse_git_url(self, git_url):
        """Parse a git URL into the owner and repo name"""
        (self.repo_owner, self.repo_name) = git_url.split("/")[-2:]        

    def load_repo_from_github(self):
        """Load a repository from GitHub"""
        st.write(f"Loading the repository {self.repo_name}...")
        documents= git_repo_reader(self.repo_owner, self.repo_name)
        st.write("Repository loaded.")
        print(f'Number of documents: {len(documents)}')
        return documents