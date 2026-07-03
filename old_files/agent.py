import duckdb
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers.string import StrOutputParser
import os

os.environ["GOOGLE_API_KEY"] = "AIzaSyCgs57MmqEEOJW5_JZ7u0qEUGdul2RQAbQ"

class LLMSQLAgent:
    def __init__(self, table):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash",temperature=0,max_tokens=None,timeout=None)
        self.table = table
        head = self.table.head()
        columns = self.table.columns
        self.prompt_start = PromptTemplate.from_template(
            """
            You are a data analyst. You will be given:
            - The names of each column in a DataFrame
            - The first 5 rows of data

            Your task: Write a short description (max 1 sentence) for each column that explains what the column represents. 
            The descriptions must use the exact column names provided (case-sensitive).

            DataFrame columns:
            {columns}

            First 5 rows:
            {head}

            Output format:
            Column name: Description
            """
        )
        self.rag_chain_init = (
            self.prompt_start
            | self.llm
            | StrOutputParser()
        )
        response = self.rag_chain_init.invoke({"columns":columns, "head":head})
        self.metadata = self.runSQLQuery(response)
        self.prompt1 = PromptTemplate.from_template(
            """You are an SQL agent. You ONLY respond with a single valid SQL query.

                You have a table named df.

                You will be given:
                - Context from the conversation: {context}
                - Natural language information about the table: {metadata}
                - Exact metadata of the table (column names and types): {info}
                - A user question: {question}

                Your job:
                1. Identify the columns in metadata that are relevant to answering the question.
                2. EXACTLY match the column names from metadata — they are case-sensitive. 
                3. If the question mentions a concept that corresponds to a column, you MUST map it to the exact name from metadata.
                4. If you cannot find an exact match in metadata, choose the closest semantically relevant column from metadata without inventing new names.
                5. Never make up or assume columns not listed in metadata.

                Rules:
                - "count" means count of UNIQUE values unless the user explicitly says "total rows" or "count all".
                - Always use the exact syntax for the SQL dialect compatible with DuckDB.
                - The query must run directly on the DataFrame df without modification.
                - Do NOT output anything except the SQL query.

                Think step-by-step:
                - First, find the relevant columns in metadata.
                - Then write the query using EXACT column names and respecting the rules above.

                Output: Only the SQL query.
"""
        )
        self.prompt2 = prompt2 = PromptTemplate.from_template(
            """You are a helpful assistant for a retail business.
            Use the following information to answer the question. You will be provided the relevant context if it exists.
            Conversational Context:
            {context}

            Information:
            {info}

            Question:
            {question}"""
        )
        self.rag_chain_first = (
            self.prompt1
            | self.llm
            | StrOutputParser()
        )
        self.rag_chain_last = (
            self.prompt2
            | self.llm
            | StrOutputParser()
        )
        self.conversation_context = ''

    def runSQLQuery(self, query):
        query = query.replace('```','')
        query = query.replace('sql','')
        print('query:', query)
        df = self.table
        try:
            result = duckdb.sql(query)
        except Exception as e:
            print("Error:",e)
            return "There has been some error please try again."
        return result.df()
    
    def chatAgent(self, user_query):
        response = self.rag_chain_first.invoke({"question":user_query, "info":self.table.info(), "metadata":self.metadata, "context":self.conversation_context})
        result = self.runSQLQuery(response)
        self.conversation_context = self.conversation_context + "User: " + user_query
        if type(result) == str:
            return result
        result_csv_str = result.to_csv(index=False)
        final_answer = self.rag_chain_last.invoke({"question":user_query, "info":result_csv_str, "context":self.conversation_context})
        self.conversation_context = self.conversation_context + "Agent: " + final_answer
        return final_answer
