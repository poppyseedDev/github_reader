from typing import Any
from langchain.vectorstores import Chroma, Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
import pinecone
import os
from load_env_var import OPENAI_API_KEY, PINECONE_API_KEY, PINECONE_API_ENV
from langchain.chains.query_constructor.base import AttributeInfo

class CreateVectorStore:
    def __init__(self) -> None:
        self.embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
        self.metadata_field_info = [
            AttributeInfo(
                name="source",
                description="Source of the file/document", 
                type="string or list[string]", 
            ),
            AttributeInfo(
                name="file_path",
                description="Path of the file/document", 
                type="string or list[string]", 
            ),
            AttributeInfo(
                name="file_name",
                description="Name of the file/document", 
                type="string or list[string]", 
            ),
            AttributeInfo(
                name="file_type",
                description="Type of the file/document",
                type="string or list[string]", 
            ),
        ]
        self.document_content_description = "Information about the repository and its contents"
        # TODO: Add a filedata sturcture to the document_content_description

    def return_metadata_field_info(self):
        """Return metadata field info"""
        return self.metadata_field_info
    
    def return_document_content_description(self):
        """Return document content description"""
        return self.document_content_description

    def create_chroma_vectorstore(self, texts) -> Any:
        """Create a Chroma index"""
        collection_name = "test"
        docsearch = Chroma.from_documents(
            texts, 
            self.embeddings, 
            collection_name=collection_name
            )
        return docsearch

    def test_chroma(self, docsearch):
        """Test Chroma"""
        query = "Of what does this repo consist of?"
        docs = docsearch.similarity_search(
            query=query,
            include_metadata=True,
        )
        print(docs)

    def query_chroma(self, docsearch, query):
        """Query Chroma"""
        docs = docsearch.similarity_search(
            query=query,
            include_metadata=True,
        )
        return docs

    def create_pinecone_vectorstore(self, texts):
        """Create a Pinecone index"""
        pinecone.init(
            api_key=PINECONE_API_KEY,
            environment=PINECONE_API_ENV
        )
        index_name = "test"
        docsearch = Pinecone.from_texts(
            [t for t in texts], 
            self.embeddings, 
            index_name=index_name
            )
        return docsearch

    def test_pinecone(self, docsearch):
        """Test Pinecone"""
        query = "Of what does this repo consist of?"
        docs = docsearch.similarity_search(
            query=query,
            include_metadata=True,
        )
        print(docs)
        