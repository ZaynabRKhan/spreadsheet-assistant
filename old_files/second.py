# from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
# from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableMap
from langchain_core.output_parsers.string import StrOutputParser
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
# import pandas as pd
import os

# os.environ["GOOGLE_API_KEY"] = "AIzaSyCgs57MmqEEOJW5_JZ7u0qEUGdul2RQAbQ"
token = "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"
loader = UnstructuredExcelLoader("E:/Startup/RAG Pipeline/Online Retail 50.xlsx", mode = "single")
docs = loader.load()
print("Document loaded")

docs = RecursiveCharacterTextSplitter(chunk_size=500).split_documents(docs)
print("Documents split")

# model_id ="mistralai/Mistral-7B-Instruct-v0.3"
# model_id = "meta-llama/Llama-2-7b-chat-hf"
model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_id, token=token)
model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", torch_dtype="auto", token=token)
# embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-exp-03-07")
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-small-en")
db = FAISS.from_documents(documents=docs, embedding=embeddings)
print("Embeddings generated")
retriever = db.as_retriever()
print("Embeddings saved")

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=512,
    do_sample=True,
    temperature=0.7,
)

llm = HuggingFacePipeline(pipeline=pipe)
# llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0,max_tokens=None,timeout=None)
# llm = OllamaLLM(model="phi3")
prompt = PromptTemplate.from_template(
    """You are a helpful assistant for a retail business.
    Use the following context to answer the question.

    Context:
    {context}

    Question:
    {question}"""
)
rag_chain = (
    {"question": lambda x: x["question"], "context": lambda x: retriever.invoke(x["question"])}
    | RunnableMap({
        "question": lambda x: x["question"],
        "context": lambda x: "\n\n".join(doc.page_content for doc in x["context"])
    })
    | prompt
    | llm
    | StrOutputParser()
)
print("Rag chain made")
while True:
    user_input = input("User: ")
    if user_input in ["quit", "exit"]:
        break
    try:
        response = rag_chain.invoke({"question": user_input})
        print("Assistant:", response)
    except Exception as e:
        print("Error:",e)