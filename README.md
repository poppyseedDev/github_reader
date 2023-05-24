## Getting started
Create a empty dir `repos`.
Create .env similar to .env.example
Run:
```
streamlit run app.py
```

### To update the list of requirements
pip3 freeze > requirements.txt  # Python3


### Process
Steps:
1. need to get git repo
2. split it to chunks, currently only works with markdown
3. create embeddings with the on the text chunks
4. create a chroma vector store
5. go into a question answer loop:
6. send the relevant chunks + question to GPT