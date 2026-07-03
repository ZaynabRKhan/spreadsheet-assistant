from transformers import T5ForConditionalGeneration, T5Tokenizer
import torch

class ResponseRephraser:
    def __init__(self, model_path="./models/friendly-t5-model"):
        self.model_path = model_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = T5Tokenizer.from_pretrained(self.model_path)
        self.model = T5ForConditionalGeneration.from_pretrained(self.model_path)
        self.model.to(self.device)
        self.model.eval()
        print("model loaded on:", self.device)

    def enhance(self, user_input, agent_response):
        input_text = f"make friendly: User: {user_input} Agent: {agent_response}"
        inputs = self.tokenizer(input_text, return_tensors="pt", max_length=64, truncation=True,padding=True)
        inputs = inputs.to(self.device)
        try:
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_length=6324,
                    num_beams=2,
                    temperature=0.3,
                    do_sample=True,
                    early_stopping=True,
                    pad_token_id=self.tokenizer.pad_token_id
                )
            
            result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return result.strip()
        except Exception as e:
            print("T5 failure")
            return agent_response