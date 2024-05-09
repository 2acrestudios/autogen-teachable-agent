# autogen-teachable-agent
This Python script is a basic implementation of AutoGen Teachable Agent using Ollama. I've had good results using the new Llama 3 models to power it. The example is using the Dolphin 2.9 model by Eric Hartford based on Llama 3. You will need AutoGen and Ollama installed.

# Custom Conversable Agent

This repository hosts two versions of a custom conversable agent named "Lou the Corgi". These agents are built using the AutoGen framework, enriched with unique identity prompts, and integrate a teachability module to adapt and learn from interactions. The advanced version extends functionality with self-reflection capabilities and direct API integration.

## Features

- **Custom Identity Prompt**: Both versions of the agent enhance user experience by responding with a unique identity.
- **Teachability**: Integrates a learning component allowing the agent to improve based on past interactions, present in both versions.
- **User Proxy Agent**: Simulates user interactions, useful for testing and development, used in both versions.
- **Self-Reflection and API Interaction**: Exclusive to the advanced version, enabling the agent to reflect on its thoughts and interact directly with APIs.

## Requirements

Ensure Python 3.8+ is installed, then install dependencies from `requirements.txt`:

```plaintext
autogen==1.0.16
virtualenv
requests  # Required for the advanced version
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

Run the agent by executing the Python script:

```bash
python custom_conversable_agent.py
```

## Code Explanation

### Environment Configuration

Disabling tokenizer parallelism to avoid multi-threading issues:

```python
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
```

### Advanced Custom Conversable Agent Class

Enhancements include API interactions and added methods for self-reflection:

```python
from autogen import ConversableAgent
import requests

class CustomConversableAgent(ConversableAgent):
    # Initialization includes storing API keys and base URL
    def __init__(self, name, llm_config, identity_prompts, *args, **kwargs):
        ...
    
    # Enhanced request handling to include self-reflection and API requests
    def handle_request(self, message):
        ...
    
    # Self-reflection method
    def reflect(self, message):
        ...
    
    # API interaction method
    def llm_predict(self, prompt):
        ...
```

### Teachability

Enabling the agent to learn and adapt from user interactions is consistent across both versions:

```python
from autogen.agentchat.contrib.capabilities.teachability import Teachability

teachability = Teachability(
    reset_db=False,
    path_to_db_dir="./tmp/interactive/teachability_db"
)
```

### Initiation Function

Starts the chat with a welcoming message:

```python
def initiate_chat():
    ...
```




