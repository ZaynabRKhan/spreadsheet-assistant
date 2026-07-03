from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd
import os
'''
LANGSMITH__TRACING = True
LANGSMITH_API_KEY = "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"
LANGSMITH_PROJECT = "RAG Pipeline Try"
'''
os.environ["GOOGLE_API_KEY"] = "AIzaSyCgs57MmqEEOJW5_JZ7u0qEUGdul2RQAbQ"
df = pd.read_excel("E:/Startup/RAG Pipeline/Online Retail.xlsx")
memory = ""
agent = create_pandas_dataframe_agent(ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0,max_tokens=None,timeout=None), 
                                      df, verbose=True, allow_dangerous_code=True)
# agent.invoke(["how many total survivors were there?", "How many of them were men and how many women?"])
print("Ask me anything about this dataset!")
while True:
    user_input = input("User:")
    if user_input in ["bye", "exit", "quit"]:
        break
    try:
        response = agent.invoke(memory + user_input)
        print(response)
        memory = memory + f"User: {user_input}\nAI: {response}"
    except Exception as e:
        print("Error:",e)