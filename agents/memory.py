class Memory:
    def __init__(self):
        self.buffer = ""
    def update(self, user_input, agent_output):
        self.buffer += f"User: {user_input}, Agent: {agent_output}\n"