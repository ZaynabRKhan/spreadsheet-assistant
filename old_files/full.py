import pandas as pd
import duckdb
# import torch
# from langchain_huggingface import HuggingFaceEmbeddings, HuggingFacePipeline
# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from langchain_core.prompts import PromptTemplate
# from langchain.schema.runnable import RunnableMap
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers.string import StrOutputParser
import os

# token = ""
os.environ["GOOGLE_API_KEY"] = ""
df = pd.read_excel("")
conversation_context = ""
def runSqlQuery(query):
    query = query.replace('```','')
    query = query.replace('sql','')
    # print("query", query)
    result = duckdb.sql(query)
    return result.df()

# model_id = "mistralai/Mistral-7B-Instruct-v0.3"
# model_id = "microsoft/DialoGPT-small"
# tokenizer = AutoTokenizer.from_pretrained(model_id, token=token)
# print("loaded model")
# model = AutoModelForCausalLM.from_pretrained(model_id, device_map="auto", torch_dtype="auto", token=token)
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0,max_tokens=None,timeout=None)
# print("loaded model")
# pipe = pipeline(
#     "text-generation",
#     model=model,
#     tokenizer=tokenizer,
#     # max_new_tokens=50, 
#     # do_sample=False, 
#     # temperature=0.9,
#     # pad_token_id=tokenizer.eos_token_id,
#     device_map="auto",
#     return_full_text=False,
# )
# print("set up the pipeline")

# llm = HuggingFacePipeline(pipeline=pipe)
# print("instantiated the llm")
prompt1 = PromptTemplate.from_template(
    """You are an SQL agent. You only respond in valid SQL queries.
    Create the relevant SQL query so that the following question can be answered.
    The DataFrame is named df. You will be provided the relevant context if it exists.
    Conversational Context:
    {context}

    Metadata of the table will be provided here:
    {metadata}
    
    CRITICAL: You MUST only use the exact column names (case-sensitive).
    RULES:
    - Table name is 'df'
    - ONLY use column names from the exact list above
    - Do NOT create or assume any column names
    - Column names are case-sensitive
    Question:
    {question}"""
)
# print("set up prompt 1")
prompt2 = PromptTemplate.from_template(
    """You are a helpful assistant for a retail business.
    Use the following information to answer the question. You will be provided the relevant context if it exists.
    Conversational Context:
    {context}

    Information:
    {info}

    Question:
    {question}"""
)

# print(pipe("What is 2 + 2?")[0]['generated_text'])

# try:
#     result = pipe(
#         "What is 2 + 2?", 
#         max_new_tokens=20,  # Much smaller
#         do_sample=False,    # Greedy decoding
#         pad_token_id=tokenizer.eos_token_id)
#     print("Pipeline result:", result)
# except Exception as e:
#     print(f"Pipeline test failed: {e}")
#     import traceback
#     traceback.print_exc()

# llm = HuggingFacePipeline(pipeline=pipe)
# print("instantiated the llm")

rag_chain = (
    prompt1
    | llm
    | StrOutputParser()
)
end_chain = (
    prompt2
    | llm
    | StrOutputParser()
)
# print("Rag chain made")
while True:
    question = input("User:")
    if question in ["quit", "exit"]:
        break
    while True:
        response = rag_chain.invoke({"question":question, "metadata":df.info(), "context":conversation_context})
        try:
            result = runSqlQuery(response)
            break
        except Exception as e:
            print("Error:", e)
    conversation_context = conversation_context + "User: " + question
    result_csv_str = result.to_csv(index=False)
    final_answer = end_chain.invoke({"question":question, "info":result_csv_str, "context":conversation_context})
    conversation_context = conversation_context + "Agent: " + final_answer
    print("Agent:", final_answer)
# question = "How many customers are in this data?"
# response = rag_chain.invoke({"question":question, "metadata":df.info(), "context":conversation_context})
# print('LLM RESPONSE:', response)
# result = runSqlQuery(response)
# conversation_context = conversation_context + "User: " + question
# result_csv_str = result.to_csv(index=False)
# final_answer = end_chain.invoke({"question":question, "info":result_csv_str, "context":conversation_context})
# conversation_context = conversation_context + "Agent: " + final_answer
# print(final_answer)
# print(conversation_context)