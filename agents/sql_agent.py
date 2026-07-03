from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=".env") 
api_key = os.getenv("GOOGLE_API_KEY")
if api_key is None:
    raise ValueError("API key not set in environment.")

class SQLAgent:
    def __init__(self, table, memory):
        self.memory = memory
        self.table = table
        self.agent = create_pandas_dataframe_agent(ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0,max_tokens=None,timeout=None), self.table, verbose=True, allow_dangerous_code=True)

    def answer(self, user_input):
        response = self.agent.invoke(user_input)
        self.memory.update("Memory:"+self.memory.buffer+"User:"+user_input, response["output"])
        return response["output"]
