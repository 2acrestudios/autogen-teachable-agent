from autogen.agentchat.contrib.capabilities.teachability import Teachability
from autogen import ConversableAgent, UserProxyAgent
import os
import requests

os.environ["TOKENIZERS_PARALLELISM"] = "false"

class CustomConversableAgent(ConversableAgent):
    def __init__(self, name, llm_config, identity_prompts, *args, **kwargs):
        super().__init__(name=name, llm_config=llm_config, *args, **kwargs)
        self.identity_prompts = identity_prompts
        # Extracting the API key and base URL for later use
        self.api_key = llm_config['config_list'][0]['api_key']
        self.base_url = llm_config['config_list'][0]['base_url']

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
        url = f"{self.base_url}/api/generate"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "dolphin-llama3:8b-v2.9-fp16",
            "prompt": prompt
        }
        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            return response.json()['text']
        except requests.exceptions.HTTPError as http_err:
            return f"HTTP error occurred: {http_err}"  # Specific HTTP error
        except Exception as err:
            return f"Other error occurred: {err}"  # Any other error

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
