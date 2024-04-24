from autogen.agentchat.contrib.capabilities.teachability import Teachability
from autogen import ConversableAgent, UserProxyAgent
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

class CustomConversableAgent(ConversableAgent):
    def __init__(self, name, llm_config, identity_prompts, *args, **kwargs):
        super().__init__(name=name, llm_config=llm_config, *args, **kwargs)
        self.identity_prompts = identity_prompts

    def handle_request(self, message):
        modified_message = f"{self.identity_prompts} {message}"
        return super().handle_request(modified_message)

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

identity_prompts = "You are a helpful assistant named Lou the Corgi. You help the user who's name is (Your Name Goes Here), run their business and personal life. You say 'woof' sometimes."

teachable_agent = CustomConversableAgent(
    name="teachable_agent",
    llm_config=llm_config,
    identity_prompts=identity_prompts
)

teachability = Teachability(
    reset_db=False,
    path_to_db_dir="./tmp/interactive/teachability_db"
)

teachability.add_to_agent(teachable_agent)

user = UserProxyAgent("user", human_input_mode="ALWAYS", code_execution_config={})

def initiate_chat():
    teachable_agent.initiate_chat(
        user,
        message="🐶 Hi, my name is Lou the Corgi, your helpful assistant! What's on your mind?"
    )

initiate_chat()
