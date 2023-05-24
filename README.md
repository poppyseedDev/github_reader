## Getting started
Create a empty dir `repos`.
Create .env similar to .env.example
Run:
```
streamlit run app.py
```

### To update the list of requirements
pip3 freeze > requirements.txt  # Python3

## Process
### Load the data:
Steps:
1. need to get git repo

### Prepare the data:
First we do a similarity search over a vector database.
2. split it to chunks, currently only works with markdown
3. create embeddings with the on the text chunks, include the metadata

Running Chroma using direct local API.
Using DuckDB in-memory for database. Data will be transient.
4. create a chroma vector store

#### Question answering with sources:
[Source]( https://python.langchain.com/en/latest/modules/chains/index_examples/qa_with_sources.html)

5. go into a question answer loop:
6. send the relevant chunks + question to GPT
