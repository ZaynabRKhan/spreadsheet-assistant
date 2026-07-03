from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
# from agent import LLMSQLAgent
from old_files.agent_lang import LLMLangAgent
import io
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
agent = None

class ChatRequest(BaseModel):
    question: str

@app.post("/upload")
async def upload_file(files: List[UploadFile] = File(...)):
    dfs = []
    for file in files:
        content = await file.read()
        if file.filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(content))
        elif file.filename.endswith((".xls", ".xlsx")):
            df = pd.read_excel(io.BytesIO(content))
        else:
            return {"error": f"Unsupported file type: {file.filename}"}
        dfs.append(df)
    global agent
    agent = LLMLangAgent(dfs[0])

    return {"message": "File uploaded and agent initialized successfully"}

@app.post("/chat")
async def chat(request: ChatRequest):
    if agent is None:
        return {"message": "No agent initialized. Upload a file first."}
    response = agent.chatAgent(request.question)
    print('got response')
    return {"response": response}