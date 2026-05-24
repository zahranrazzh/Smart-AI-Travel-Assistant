from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS


def create_vectorstore(pdf_path):

    loader = PyPDFLoader(pdf_path)

    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    texts = text_splitter.split_documents(documents)

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001"
    )

    vectorstore = FAISS.from_documents(
        texts,
        embeddings
    )

    return vectorstore


def search_docs(vectorstore, query):

    docs = vectorstore.similarity_search(
        query,
        k=3
    )

    context = ""

    for doc in docs:
        context += doc.page_content + "\n"

    return context