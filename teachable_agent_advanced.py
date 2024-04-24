from autogen.agentchat.contrib.capabilities.teachability import Teachability
from autogen import ConversableAgent, UserProxyAgent
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

class CustomConversableAgent(ConversableAgent):
    def __init__(self, name, llm_config, identity_prompts, *args, **kwargs):
        super().__init__(name=name, llm_config=llm_config, *args, **kwargs)
        self.identity_prompts = identity_prompts

    def handle_request(self, message):
        if message.startswith("self-reflect:"):
            reflection = self.reflect(message[len("self-reflect:"):].strip())
            return reflection
        elif message.startswith("teach:") or message.startswith("remember:"):
            return super().handle_request(message)
        else:
            modified_message = f"{self.identity_prompts} {message}"
            return super().handle_request(modified_message)

    def reflect(self, message):
        reflection_prompt = f"Upon self-reflection regarding {message}: "
        # Get the response from the LLM predict method
        response = self.llm_predict(reflection_prompt)
        # Concatenate the prompt and the response, and wrap them in grey
        output = f"{reflection_prompt}{response}"
        return output

    def llm_predict(self, prompt):
        # Simulate an LLM prediction, replace with actual prediction logic as necessary
        return "This is a simulated response to the reflection prompt."

config_list = [
    {
        "model": "dolphin-llama3:8b-v2.9-fp16",
        "api_key": "ollama",
        "base_url": "http://localhost:11434/v1"
    }
]

llm_config = {
    "config_list": config_list,
    "timeout": 120
}

identity_prompts = "You are a teachable user assistant named Lou. You are capable of storing and retrieving memories, self reflecting, and learning."

teachable_agent = CustomConversableAgent(
    name="Lou",
    llm_config=llm_config,
    identity_prompts=identity_prompts
)

teachability = Teachability(
    reset_db=False,
    path_to_db_dir="./tmp/interactive/teachability_db"
)

teachability.add_to_agent(teachable_agent)

user = UserProxyAgent("Marc", human_input_mode="ALWAYS", code_execution_config={})

def initiate_chat():
    teachable_agent.initiate_chat(
        user,
        message="🐶 Hi, my name is Lou the Corgi, your helpful, teachable assistant! What's on your mind?"
    )

initiate_chat()
