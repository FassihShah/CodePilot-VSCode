from fastapi import FastAPI
from pydantic import BaseModel
from backend.agents.boilerplate_agent import get_boilerplate_graph
from backend.agents.code_editor_agent import get_code_editor_graph
from backend.agents.code_explainer_agent import build_code_explainer_graph
from backend.agents.embed_saver_agent import get_embed_saver_graph
from backend.agents.chat_agent import get_chat_graph



boilerplate_graph = get_boilerplate_graph()
code_editor_graph = get_code_editor_graph()
code_explainer_graph = build_code_explainer_graph()
embed_store_graph = get_embed_saver_graph()
chat_graph = get_chat_graph()



app = FastAPI()


# Boilerplate Generator

class BoilerplateRequest(BaseModel):
    prompt: str

class BoilerplateResponse(BaseModel):
    files: dict

@app.post("/generate-boilerplate/", response_model=BoilerplateResponse)
async def generate_boilerplate(req: BoilerplateRequest):
    result = boilerplate_graph.invoke({"user_input": req.prompt})
    return {"files": result.get("files", {})}



# Code Editor Agent

class CodeEditorRequest(BaseModel):
    full_code: str
    selected_code: str
    instruction: str

class CodeEditorResponse(BaseModel):
    updated_code: str
    full_updated_code: str
    explanation: str

@app.post("/edit-code/", response_model=CodeEditorResponse)
async def edit_code(req: CodeEditorRequest):
    result = code_editor_graph.invoke({
        "full_code": req.full_code,
        "selected_code": req.selected_code,
        "instruction": req.instruction
    })
    return {"updated_code": result.get("updated_selection", ""), "explanation": result.get("explanation", ""),"full_updated_code": result.get("updated_code", "")}


# Code Explainer Agent

class CodeExplainerRequest(BaseModel):
    selected_code: str
    full_code: str

class CodeExplainerResponse(BaseModel):
    explanation: str


@app.post("/explain-code/", response_model=CodeExplainerResponse)
async def explain_code(req: CodeExplainerRequest):
    result = code_explainer_graph.invoke({
        "selected_code": req.selected_code,
        "full_code": req.full_code
    })
    return {"explanation": result.get("explanation", "")}


# Embed and Store Agent

class EmbedStoreRequest(BaseModel):
    files: dict

class EmbedStoreResponse(BaseModel):
    status: str

@app.post("/embed-and-store/", response_model=EmbedStoreResponse)
async def embed_and_store(req: EmbedStoreRequest):
    result = embed_store_graph.invoke({
        "files": req.files
    })
    return {"status": "success"}



# Chat Agent

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str

@app.post("/chat-with-code/", response_model=ChatResponse)
async def chat_with_code(req: ChatRequest):
    result = chat_graph.invoke({
        "query": req.query
    })
    return {"answer": result.get("answer", "Sorry, couldn't generate a response.")}


