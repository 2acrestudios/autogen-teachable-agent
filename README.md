# autogen-teachable-agent
This Python script is a basic implementation of AutoGen Teachable Agent using Ollama. I've had good results using the new Llama 3 models to power it. The example is using the Dolphin 2.9 model by Eric Hartford based on Llama 3. You will need AutoGen and Ollama installed.


Below is a sample `README.md` document for the Python code provided, tailored for inclusion in your GitHub repository. This document will guide users on setting up and understanding the functionality of your custom conversable agent based on the AutoGen framework.

---

# Custom Conversable Agent

This repository contains the implementation of a custom conversable agent named "Lou the Corgi". This agent, built using the AutoGen framework, enriches interactions with a unique identity and integrates a teachability module to facilitate conversational adaptability.

## Features

- **Custom Identity Prompt**: The agent responds with a unique identity, enhancing the user experience.
- **Teachability**: Enables the agent to learn from interactions, improving response accuracy over time.
- **User Proxy Agent**: Allows the agent to simulate user interactions for testing and development purposes.

## Requirements

To set up the project environment, ensure you have Python 3.8+ installed, and then install the dependencies from the `requirements.txt` file included in this repository. Do it in a virtual environment of your choice, or don't. But if you build more on top of this, you'll appreciate it later!

```plaintext
autogen==1.0.16
```

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the cloned directory:
   ```bash
   cd <repository-directory>
   ```
3. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

To run the agent, execute the Python script:

```bash
python custom_conversable_agent.py
```

## Code Explanation

### Setting Environment Variables

```python
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
```
This line disables tokenizer parallelism to avoid multi-threading issues, commonly required in environments with limited threading support.

### Custom Conversable Agent Class

```python
from autogen import ConversableAgent

class CustomConversableAgent(ConversableAgent):
    def __init__(self, name, llm_config, identity_prompts, *args, **kwargs):
        super().__init__(name=name, llm_config=llm_config, *args, **kwargs)
        self.identity_prompts = identity_prompts

    def handle_request(self, message):
        modified_message = f"{self.identity_prompts} {message}"
        return super().handle_request(modified_message)
```
This class extends `ConversableAgent` to prepend identity prompts to each message, embedding a unique character for the agent.

### Teachability

```python
from autogen.agentchat.contrib.capabilities.teachability import Teachability

teachability = Teachability(
    reset_db=False,
    path_to_db_dir="./tmp/interactive/teachability_db"
)
```
Integrates a learning component that allows the agent to improve based on past interactions. For more information, refer to the [AutoGen Teachability Documentation](https://example.com/teachability).

### Initiation Function

```python
def initiate_chat():
    teachable_agent.initiate_chat(
        user,
        message="🐶 Hi, my name is Lou the Corgi, your helpful assistant! What's on your mind?"
    )
```
This function starts the chat interface with a welcoming message, initiating the user-agent interaction.
---



