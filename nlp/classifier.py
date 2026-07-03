from sentence_transformers import SentenceTransformer
import pickle

class QueryClassifier:
    def __init__(self, model_path = "./models/query_classifier_miniLM.pkl"):
        self.embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        with open(model_path, "rb") as f:
            self.query_classifier = pickle.load(f)
    def createEmbeddings(self, query):
        return self.embedding_model.encode(query)
    def mapLabels(self, prediction, model_path = "./models/label_encoder.pkl"):
        with open(model_path, "rb") as f:
            self.label_encoder = pickle.load(f)
        return self.label_encoder.inverse_transform([prediction])[0]
    def predictQuery(self, query):
        embedded_query = self.createEmbeddings(query)
        pred = self.query_classifier.predict(embedded_query.reshape(1, -1))[0]
        pred = self.mapLabels(pred)
        print("Predicted:", pred)
        return pred