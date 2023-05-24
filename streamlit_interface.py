import streamlit as st
from load_into_docs import git_repo_reader, clone_git_repo, load_git_from_disk
from process_gpt import gpt_answer, parse_into_nodes, add_to_docsstore, define_multiple_indexes, test_some_queries
from load_into_docs import chunk_data_into_smaller_docs, chunk_data_based_on_markdown
from create_vectorstore import create_embeddings, create_chroma_vectorstore, test_chroma, test_pinecone, query_chroma

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

            # Load the repository from GitHub
            path_of_repo, branch = clone_git_repo(git_url=git_url)
            documents = load_git_from_disk(path_of_repo=path_of_repo, branch=branch)

            #documents = self.load_repo_from_github()
            st.write(f"Number of documents: {len(documents)}")
            st.write("Chunking documents into smaller chunks...")
            #texts = chunk_data_into_smaller_docs(documents)
            texts = chunk_data_based_on_markdown(documents)
            # st.write(texts)
            st.write("Chunking complete.")

            embeddings = create_embeddings()
            docsearch = create_chroma_vectorstore(texts=texts, embeddings=embeddings)
            st.write("Index created.")
            #test_chroma(docsearch=docsearch)

            # Run gpt chatbot
            query = st.text_input("Enter a question: ")
            if query:
                relevant_docs = query_chroma(docsearch=docsearch, query=query)
                #answer = gpt_answer(docs=relevant_docs, query=query)
                #st.write(answer)

                with st.expander("Sources"):
                    st.info(relevant_docs)



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