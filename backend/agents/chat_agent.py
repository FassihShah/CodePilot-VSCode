from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from typing import TypedDict
from langgraph.graph import StateGraph, END



class ChatState(TypedDict):
    query: str
    answer: str



def load_vectorstore():
    embedding = GoogleGenerativeAIEmbeddings(model="gemini-embedding-001")
    return FAISS.load_local("vectorstores/codebase_faiss", embedding, allow_dangerous_deserialization=True)




def chat_with_context(state: ChatState) -> ChatState:
    """Load and pass context with query to model"""

    query = state["query"]

    
    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 5})
    docs = retriever.get_relevant_documents(query)

    context = "\n\n".join([doc.page_content for doc in docs])


    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)

    prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""
You are a coding assistant. Use the following context from the user's codebase to answer the question.
Note: Answers should be concise and to the point, but include all necessary information. 

Context:
{context}

Question:
{question}

Answer:"""
    )

    chain = prompt | llm
    response = chain.invoke({"context": context, "question": query})

    state["answer"] = response.content
    return state



def get_chat_graph():
    graph = StateGraph(ChatState)

    graph.add_node("chat", chat_with_context)
    graph.set_entry_point("chat")
    graph.add_edge("chat", END)

    return graph.compile()
