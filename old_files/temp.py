# import pandas as pd
# df = pd.read_excel("E:/Startup/RAG Pipeline/Online Retail.xlsx")
# df = df.head(50)
# df.to_excel("E:/Startup/RAG Pipeline/Online Retail 50.xlsx", index = False)

# from langchain.prompts import PromptTemplate

# prompt = PromptTemplate.from_template("Q: {question}\nContext: {context}")
# print(prompt.format(**{"question": "How many sales?", "context": "Data chunk here"}))

from google import genai
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyCgs57MmqEEOJW5_JZ7u0qEUGdul2RQAbQ"
chat_agent = genai.Client()
data_context = chat_agent.models.generate_content(model="gemini-2.5-flash", contents="What can you do?")
print(data_context.text)
print(type(data_context.text))
# [{"role":"user", "parts":[f"I what can you do?\n"]}]