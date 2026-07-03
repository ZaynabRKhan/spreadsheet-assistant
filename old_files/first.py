from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd
import os

os.environ["GOOGLE_API_KEY"] = ""
df = pd.read_excel("")
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