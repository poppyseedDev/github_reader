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
### Load the documents:
Steps:
1. user specifies repo url, if repo already loaded - no need for repo

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


## Explaining how it works with the following medium article:
Source: https://medium.com/p/188c6707cc5a

**map_reduce**: It separates texts into batches (as an example, you can define batch size in llm=OpenAI(batch_size=5)), feeds each batch with the question to LLM separately, and comes up with the final answer based on the answers from each batch.
**refine** : It separates texts into batches, feeds the first batch to LLM, and feeds the answer and the second batch to LLM. It refines the answer by going through all the batches.
**map-rerank**: It separates texts into batches, feeds each batch to LLM, returns a score of how fully it answers the question, and comes up with the final answer based on the high-scored answers from each batch.


OpenAI's Langchain provides various methods for performing question-answering tasks on external documents:

1. **load_qa_chain**: It enables QA over multiple documents. However, there might be issues with long documents exceeding token limits. This issue can be solved using different chain types such as "map_reduce", "refine", and "map-rerank". Each of these approaches breaks the document into batches and processes them in different ways. Alternatively, RetrievalQA can be used to retrieve relevant text chunks before passing them into the language model.

2. **RetrievalQA**: Issue with **load_qa_chain** -> can be costly ->
A better solution is to retrieve relevant text chunks first and only use the relevant text chunks in the language model.

This method uses load_qa_chain under the hood, retrieves the most relevant chunk of text, and feeds those to the language model. It involves several steps: splitting the documents into chunks, selecting embeddings, creating a vector store to use as the index, exposing this index in a retriever interface, and creating a chain to answer questions. 

   There are several options to customize this process, including choosing different embeddings, text splitters, vector stores, retrievers, and chain types.

3. **VectorstoreIndexCreator**: This method is a wrapper that simplifies the functionality of RetrievalQA into a higher-level interface, allowing you to get started in just three lines of code. You can specify different options in this wrapper.

4. **ConversationalRetrievalChain**: This is similar to RetrievalQA but adds an additional parameter, chat_history, for follow-up questions. It combines the capabilities of conversation memory and RetrievalQAChain, allowing the language model to retain previous conversation history for context.

These methods allow you to efficiently manage and process large amounts of text for question-answering tasks, optimizing for both cost and accuracy by using techniques like document batching and retrieval of relevant text chunks.


## TODO:
 - allow for processing also .js and other extensions:
    - separate according for python files by def
    - js files by function definitions etc
 - template for create me a better README for this document.