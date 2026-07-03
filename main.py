from agents.manager import AgentManager
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import List
import pandas as pd
import io

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
    agent = AgentManager(dfs[0])

    return {"message": "File uploaded and agent initialized successfully"}

@app.post("/chat")
async def chat(request: ChatRequest):
    if agent is None:
        return {"message": "No agent initialized. Upload a file first."}
    response = agent.chat(request.question)
    print('got response')
    return {"response": response}