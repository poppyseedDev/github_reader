import streamlit as st
from process_gpt import git_repo_reader, load_docs, parse_into_nodes, add_to_docsstore, define_multiple_indexes, test_some_queries

class StreamlitInterface:
    def __init__(self):
        self.git_url = None
    
    def start_interface(self):
        st.title("💻🦾 Load a GitHub repository")
        self.git_url = st.text_input("Enter the GitHub URL of the repository: ")
        if self.git_url:
            documents = self.load_repo_from_github()
            return documents

    def parse_git_url(self):
        """Parse a git URL into the owner and repo name"""
        (repo_owner, repo_name) = self.git_url.split("/")[-2:]
        return (repo_owner, repo_name)
        

    def load_repo_from_github(self):
        """Load a repository from GitHub"""
        (repo_owner, repo_name) = self.parse_git_url(self.git_url)
        st.write(f"Loading the repository {repo_name}...")
        documents= git_repo_reader(repo_owner, repo_name)
        st.write("Repository loaded.")
        print(f'Number of documents: {len(documents)}')
        return documents