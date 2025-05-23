import os

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

current_script_dir = os.path.dirname(os.path.abspath(__file__))

DATA_DIR = os.path.abspath(os.path.join(current_script_dir, '..', 'data'))
PERSISTENT_DIR = os.path.abspath(os.path.join(current_script_dir, '..', 'vector_db'))


def load_and_split_docs():
    docs = []
    for filename in os.listdir(DATA_DIR):
        if filename.endswith(".pdf"):
            path = os.path.join(DATA_DIR, filename)
            loader = PyPDFLoader(path)
            doc_pages = loader.load_and_split()
            for doc in doc_pages:
                doc.metadata['fileName'] = os.path.basename(path)
            docs.extend(doc_pages)

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunked_documents = text_splitter.split_documents(docs)
    return chunked_documents


def create_vectorstore(docs):
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)
    return vectorstore


def persist_vector_db(db):
    db.save_local(PERSISTENT_DIR)


def load_vector_db(persist_directory):
    embeddings = OpenAIEmbeddings()
    return FAISS.load_local(persist_directory, embeddings, allow_dangerous_deserialization=True)


def create_and_load_vectorstore():
    documents = load_and_split_docs()
    vectorstore = create_vectorstore(documents)
    persist_vector_db(vectorstore)

    return vectorstore
