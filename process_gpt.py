from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

import os
from llama_index.readers.base import BaseReader
#from llama_index import download_loader, GPTVectorStoreIndex
import pickle
from llama_index import SimpleDirectoryReader, ServiceContext, LLMPredictor
from llama_index.node_parser import SimpleNodeParser
from llama_index.storage.docstore import SimpleDocumentStore
from llama_index.storage.storage_context import StorageContext
from llama_index import SimpleDirectoryReader, ServiceContext, LLMPredictor
from llama_index import GPTVectorStoreIndex, GPTListIndex, GPTSimpleKeywordTableIndex
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter, MarkdownTextSplitter, TextSplitter
from git import Repo
from langchain.document_loaders import GitLoader
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.chains.qa_with_sources import load_qa_with_sources_chain
from langchain.chains import ConversationalRetrievalChain

from load_env_var import OPENAI_API_KEY

# as a response to issue https://github.com/hwchase17/langchain/issues/4887 using Lark, which seems to solve the problem
from lark import Lark, Transformer, v_args


# def parse_into_nodes(documents):
#     """Parse documents into nodes"""
#     nodes = SimpleNodeParser().get_nodes_from_documents(documents)
#     return nodes

# def add_to_docsstore(nodes):
#     """Add nodes to docsstore"""
#     docstore = SimpleDocumentStore()
#     docstore.add_documents(nodes)
#     return docstore

# def define_multiple_indexes(nodes, docstore):
#     """Define multiple indexes"""
#     storage_context = StorageContext.from_defaults(docstore=docstore)
#     list_index = GPTListIndex(nodes, storage_context=storage_context)
#     vector_index = GPTVectorStoreIndex(nodes, storage_context=storage_context) 
#     keyword_table_index = GPTSimpleKeywordTableIndex(nodes, storage_context=storage_context) 
#     len(storage_context.docstore.docs)
    
#     return (list_index, vector_index, keyword_table_index)

class ChatGPT:
    def __init__(self):
        self.llm = OpenAI(temperature=0.9, openai_api_key=OPENAI_API_KEY)
        self.retriever = None
        self.chat_history = []
        #self.llm_predictor_chatgpt = LLMPredictor(llm=ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0, model_name="gpt-3.5-turbo"))

    def create_self_querying_retriever(self, vectorstore, document_content_description, metadata_field_info):
        """Create a self-querying retriever
        Now we can instantiate our retriever. To do this we’ll need to provide some information upfront about the metadata fields that our documents support and a short description of the document contents.
        """
        self.retriever = SelfQueryRetriever.from_llm(
            llm=self.llm,
            vectorstore=vectorstore,
            document_contents=document_content_description,
            metadata_field_info=metadata_field_info,
            nable_limit=True,
            verbose=True
        )

    def create_simple_retriever(self, vectorstore):
        """Create simple retriever based on similartiy search"""
        self.retriever = vectorstore.as_retriever(search_type="similarity",
                            search_kwargs={"k": 5})

    def call_retriever(self, query):
        """Call retriever"""
        if self.retriever is None:
            raise Exception("Retriever is not initialized. Please call create_self_querying_retriever() first.")
        relevant_docs = self.retriever.get_relevant_documents(query=query)
        return relevant_docs

    def test_some_queries(self, list_index, vector_index, keyword_table_index):
        """Test some queries"""
        llm_predictor_chatgpt = LLMPredictor(llm=ChatOpenAI(api_key=OPENAI_API_KEY, temperature=0, model_name="gpt-3.5-turbo"))
        service_context_chatgpt = ServiceContext.from_defaults(llm_predictor=llm_predictor_chatgpt, chunk_size_limit=1024)
        query_engine = list_index.as_query_engine()

        while (True):
            input_test = input("Enter question: ")

            response = query_engine.query(input_test) 
            print(response)

    def gpt_answer(self, docs, query):
        chain = load_qa_with_sources_chain(
            self.llm,
            chain_type="stuff"
        )
        query = query
        answer = chain({
            "input_documents": docs,
            "question": query
            }, return_only_outputs=True)
        
        #chain = RetrievalQAWithSourcesChain.from_chain_type(OpenAI(temperature=0), chain_type="stuff", retriever=docsearch.as_retriever())


        #answerMe = RetrievalQA.from_chain_type(self.llm, chain_type="stuff", retriever=docs.as_retriever())
        #answer = answerMe.run(query)

        #chain = load_qa_chain(llm, chain_type="stuff")
        #answer = chain.run(input_documents=docs, question=query)
        return answer["output_text"]
    
    def gpt_conversational_retrieval_chain(self):
        """Conversational retrieval chain"""
        qa = ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.retriever,
            return_source_documents=True
        )
        return qa

    def gpt_question_remember_history(self, qa, query):
        result = qa({"question": query, "chat_history": self.chat_history})
        self.chat_history = [(query, result["answer"])]
        return result