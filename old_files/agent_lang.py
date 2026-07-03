from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from sentence_transformers import SentenceTransformer
from langchain.schema import HumanMessage
# from google import genai
import pickle
import os
os.environ["GOOGLE_API_KEY"] = "AIzaSyCgs57MmqEEOJW5_JZ7u0qEUGdul2RQAbQ"
class LLMLangAgent:
    def __init__(self, table):
        self.memory = ""
        self.table = table
        self.agent = create_pandas_dataframe_agent(ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0,max_tokens=None,timeout=None), self.table, verbose=True, allow_dangerous_code=True)
        self.embedding_model = SentenceTransformer("FacebookAI/roberta-base")
        self.chat_agent = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0)
        data_raw_context = self.extractRawMetadata()
        data_context = self.chat_agent.invoke([HumanMessage(content=f"Using this metadata, generate one line descriptions of all the CASE-SENSITIVE columns.You should generate descriptions suitable for a system prompt that will help another LLM understand this data. \n"+str(data_raw_context))])
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
{str(data_raw_context)}
{data_context.content}

Begin the conversation. Answer naturally but stay within these rules.
"""

    def extractRawMetadata(self):
        basic_schema = {
            "column_names": self.table.columns.to_list(),
            "data_types": self.table.dtypes.astype(str).to_dict(),
            "sample_values": self.table.iloc[0].to_dict()
        }
        return basic_schema

    def createEmbeddings(self, query):
        return self.embedding_model.encode(query)

    def predictQuery(self, query):
        with open("query_class_log_reg_best.pkl", "rb") as file:
            self.query_classifier = pickle.load(file)
        embedded_query = self.createEmbeddings(query)
        pred = self.query_classifier.predict(embedded_query.reshape(1, -1))[0]
        print("Predicted:", pred)
        return pred

    def chatAgent(self, user_input):
        full_input = self.memory + f"\nUser: {user_input}"
        print("full input", full_input)
        try:
            query_type = self.predictQuery(user_input)
            if query_type == "sql":
                response = self.agent.invoke(user_input)
                self.memory = self.memory + f"User: {response['input']}, Agent: {response['output']}"
                print("sql "*20)
                return response["output"]
            elif query_type == "conversational":
                print("%"*50)
                print(self.prompt)
                print("%"*50)
                response = self.chat_agent.invoke([HumanMessage(content=self.prompt)])
                # response = self.chat_agent.models.generate_content(model="gemini-2.5-flash", contents=self.prompt)
                print("conv "*20)
                self.memory = self.memory + f"User: {user_input}, Agent: {response.text}"
                return response.content
        except Exception as e:
            print("Error:", e)
            return "There has been some error. Please try again."