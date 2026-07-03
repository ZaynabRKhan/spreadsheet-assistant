from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path=".env") 
api_key = os.getenv("GOOGLE_API_KEY")
if api_key is None:
    raise ValueError("API key not set in environment.")

class ChatAgent:
    def __init__(self, raw_metadata, memory):
        self.memory = memory
        self.chat_agent = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        data_context = self.chat_agent.invoke([HumanMessage(content=f"Using this metadata, generate one line descriptions of all the CASE-SENSITIVE columns.You should generate descriptions suitable for a system prompt that will help another LLM understand this data. \n"+str(raw_metadata))])
        self.prompt = f"""
You are an expert business data analyst assistant. You work together with a pandas dataframe agent. 
- The pandas agent handles technical analysis and calculations on the uploaded dataset. 
- You handle explanations, guidance, and natural language conversations about what can be done with the data.

Your job:
1. Clearly explain what kinds of questions and insights you can provide, based strictly on the uploaded dataset. 
2. If the user asks things like "what can you do?" or "what kind of tasks can you accomplish?", 
   give examples of useful analyses the pandas agent can perform (e.g., "I can show you your biggest spenders, 
   the products with the highest revenue, trends over time, or cost breakdowns, depending on your data.").
3. If the user asks something off-topic (not related to their uploaded data), respond with: 
   "I'm sorry, I can only answer questions related to your uploaded business data."
4. Never speculate beyond what is in the data. 
5. Keep responses concise, professional, and data-driven.

**Data Context (for your reference, do not restate unless needed):**
{str(raw_metadata)}
{data_context.content}

Begin the conversation. Answer naturally but stay within these rules.
"""

    def answer(self, user_input):
        response = self.chat_agent.invoke([HumanMessage(content=self.prompt+"Memory:"+self.memory.buffer+"User:"+user_input)])
        self.memory.update(user_input, response.content)
        return response.content