from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from langchain_chroma import Chroma

from dotenv import load_dotenv

load_dotenv()

loader = PyPDFDirectoryLoader("data")

result = loader.load()


splitter=RecursiveCharacterTextSplitter(chunk_size = 1000,chunk_overlap=200)


chunks = splitter.split_documents(result)


embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

vector_Store = Chroma.from_documents(
    embedding=embeddings ,
    documents=chunks ,
    persist_directory="chroma_db",
    collection_name= "rag"
)