from file_processing import clone_github_repo
from process_gpt import git_repo_reader, load_docs, parse_into_nodes, add_to_docsstore, define_multiple_indexes, test_some_queries
import os
import streamlit as st


def get_files_and_folders(directory):
    return os.listdir(directory)

def clone_a_repo_or_not():
    clone_or_no = input("Do you want to clone a repository? (y/n)")
    if clone_or_no == "y":
        # clone repo
        github_url = input("Enter the GitHub URL of the repository: ")
        repo_name = github_url.split("/")[-1]
        print("Cloning the repository...")
        clone_github_repo(github_url, f"repos")
    else:
        print("Assuming you have cloned the repository already.")
        print("Loading the repository...")
        repo_name = "repos"
        files_in_dir = get_files_and_folders(repo_name)
        print(f"Files in directory: {files_in_dir}")
        chosen_dir = input(f"Enter the directory you want to load (choose from {files_in_dir}): ")
        repo_name = f"{repo_name}/{chosen_dir}"
        documents = load_docs(repo_name)
        print("Repository loaded.")
    
        # parse into nodes
        nodes = parse_into_nodes(documents)
        docstore = add_to_docsstore(nodes)
        list_index, vector_index, keyword_table_index = define_multiple_indexes(nodes, docstore)
        test_some_queries(list_index, vector_index, keyword_table_index)


def parse_git_url(git_url):
    (repo_owner, repo_name) = git_url.split("/")[-2:]
    return (repo_owner, repo_name)
    

def load_repo_from_github(git_url):
    (repo_owner, repo_name) = parse_git_url(git_url)
    st.write(f"Loading the repository {repo_name}...")
    documents= git_repo_reader(repo_owner, repo_name)
    st.write("Repository loaded.")
    print(f'Number of documents: {len(documents)}')
    return documents


def parse_into_nodes_and_define_indexes(documents):
    # parse into nodes
    nodes = parse_into_nodes(documents)
    docstore = add_to_docsstore(nodes)
    list_index, vector_index, keyword_table_index = define_multiple_indexes(nodes, docstore)
    test_some_queries(list_index, vector_index, keyword_table_index)


def main():
    st.title("💻🦾 Load a GitHub repository")
    git_url = st.text_input("Enter the GitHub URL of the repository: ")

    if git_url:
        load_repo_from_github(git_url)
