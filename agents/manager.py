from agents.sql_agent import SQLAgent
from agents.chat_agent import ChatAgent
from agents.memory import Memory
from nlp.classifier import QueryClassifier
from nlp.rephraser import ResponseRephraser

class AgentManager:
    def __init__(self, table):
        self.memory = Memory()
        raw_metadata = self.extractRawMetadata(table)
        self.sql_agent = SQLAgent(table, self.memory)
        self.chat_agent = ChatAgent(raw_metadata, self.memory)
        self.classifier = QueryClassifier()
        self.response_rephraser = ResponseRephraser()

    def extractRawMetadata(self, table):
        basic_schema = {
            "column_names": table.columns.to_list(),
            "data_types": table.dtypes.astype(str).to_dict(),
            "sample_values": table.iloc[0].to_dict()
        }
        return basic_schema
    
    def chat(self, user_input):
        prediction = self.classifier.predictQuery(user_input)
        if prediction == "conversational":
            response = self.chat_agent.answer(user_input)
            return response
        elif prediction == "sql":
            response = self.sql_agent.answer(user_input)
            response = self.response_rephraser.enhance(user_input, response)
            return response