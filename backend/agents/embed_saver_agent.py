from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from typing import TypedDict, List, Dict
from langchain.docstore.document import Document
from langgraph.graph import StateGraph, END
import os

EMBED_STORE_PATH = "vectorstores/codebase_faiss"


class EmbedSaverState(TypedDict):
    files: Dict[str, str]  
    loaded_docs: List[Document]
    split_docs: List[Document]


def read_documents(state: EmbedSaverState) -> EmbedSaverState:
    """Convert input files to LangChain Documents"""

    docs = []

    for filename, content in state["files"].items():
        docs.append(Document(page_content=content, metadata={"source": filename}))

    state["loaded_docs"] = docs
    return state


def split_documents(state: EmbedSaverState) -> EmbedSaverState:
    """Split documents into small chunks"""

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    state["split_docs"] = splitter.split_documents(state["loaded_docs"])
    return state


def embed_and_save(state: EmbedSaverState) -> EmbedSaverState:
    """Embed all chunks and store them in FAISS"""

    embedder = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")

    vectorstore = FAISS.from_documents(state["split_docs"], embedder)

    os.makedirs(EMBED_STORE_PATH, exist_ok=True)
    vectorstore.save_local(EMBED_STORE_PATH)

    return state


def get_embed_saver_graph():
    graph = StateGraph(EmbedSaverState)

    graph.add_node("read_documents", read_documents)
    graph.add_node("split_documents", split_documents)
    graph.add_node("embed_and_save", embed_and_save)

    graph.set_entry_point("read_documents")
    graph.add_edge("read_documents", "split_documents")
    graph.add_edge("split_documents", "embed_and_save")
    graph.add_edge("embed_and_save", END)

    return graph.compile()
