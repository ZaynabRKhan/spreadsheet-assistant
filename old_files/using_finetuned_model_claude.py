# Using your fine-tuned T5 model in your app
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer

class FriendlyResponseEnhancer:
    def __init__(self, model_path="./friendly-t5-final"):
        """Initialize the fine-tuned model"""
        print("Loading fine-tuned model...")
        
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.tokenizer = T5Tokenizer.from_pretrained(model_path)
        self.model = T5ForConditionalGeneration.from_pretrained(model_path)
        self.model.to(self.device)
        self.model.eval()  # Set to evaluation mode
        
        print(f"Model loaded on {self.device}")
    
    def enhance_response(self, user_query: str, agent_response: str) -> str:
        """Convert pandas agent response to friendly format"""
        
        # Format input the same way as training data
        input_text = f"make friendly: User: {user_query} Agent: {agent_response}"
        
        # Tokenize
        inputs = self.tokenizer(
            input_text, 
            return_tensors="pt", 
            max_length=128, 
            truncation=True,
            padding=True
        )
        inputs = inputs.to(self.device)
        
        # Generate response
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=64,
                num_beams=2,        # Faster than 4, still good quality
                temperature=0.3,    # Low temperature for consistency
                do_sample=True,
                early_stopping=True,
                pad_token_id=self.tokenizer.pad_token_id
            )
        
        # Decode and clean up
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return result.strip()

# Initialize once when your app starts
enhancer = FriendlyResponseEnhancer()

# Use in your main query processing function
def process_sql_query(user_query: str, data):
    """Your main query processing function"""
    
    # Your existing pandas agent call
    raw_response = pandas_agent.run(user_query)
    
    # Enhance with your fine-tuned model
    friendly_response = enhancer.enhance_response(user_query, raw_response)
    
    return friendly_response

# Example usage
if __name__ == "__main__":
    # Test the enhancer
    test_cases = [
        ("How many customers are in this data?", "4"),
        ("What's the total revenue?", "25000"),
        ("Show me the average age", "42.3"),
        ("List the top products", "['iPhone', 'MacBook', 'iPad']")
    ]
    
    for query, response in test_cases:
        enhanced = enhancer.enhance_response(query, response)
        print(f"Query: {query}")
        print(f"Raw: {response}")
        print(f"Enhanced: {enhanced}")
        print("-" * 50)

# For faster inference (optional optimization)
class FastFriendlyEnhancer(FriendlyResponseEnhancer):
    """Optimized version for faster inference"""
    
    def enhance_response(self, user_query: str, agent_response: str) -> str:
        input_text = f"make friendly: User: {user_query} Agent: {agent_response}"
        
        inputs = self.tokenizer(
            input_text, 
            return_tensors="pt", 
            max_length=128, 
            truncation=True
        )
        inputs = inputs.to(self.device)
        
        # Faster generation settings
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_length=48,      # Shorter max length
                num_beams=1,        # Greedy search (fastest)
                temperature=0.1,    # Very low temperature
                do_sample=False,    # Deterministic
                early_stopping=True
            )
        
        result = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return result.strip()