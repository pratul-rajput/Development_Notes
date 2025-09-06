Perfect 👍 now let’s build the **complete guide from scratch**, but this time with **Ollama running inside Podman** instead of directly on your host.
This way you’ll have a **clean, isolated setup** that you can reuse years later.

---

# 🚀 Running Autogen with Ollama (via Podman + LiteLLM)

This setup connects **Autogen** → **LiteLLM Proxy** → **Ollama in Podman container**.

---

## 🔹 1. Install Dependencies (on host machine)

Run in PowerShell / CMD:

```bash
pip install litellm pyautogen
```

👉 No need to install Ollama on host, since it’ll run inside Podman.

---

## 🔹 2. Run Ollama in Podman

Start Ollama container and expose it:

```bash
podman run -d --name ollama \
  -p 11434:11434 \
  ollama/ollama
```

* `-p 11434:11434` → maps Ollama API to host machine
* Ollama API will now be available at:

  ```
  http://127.0.0.1:11434
  ```

---

## 🔹 3. Pull the lightest model (tinyllama) inside Podman

Exec into the container:

```bash
podman exec -it ollama ollama pull tinyllama
```

Check models inside container:

```bash
podman exec -it ollama ollama list
```

✅ You should see `tinyllama:latest` (\~637 MB).

---

## 🔹 4. Start LiteLLM Proxy (on host)

Now run LiteLLM on host, pointing it to Ollama inside Podman:

```bash
litellm --model ollama/tinyllama:latest --port 4000
```

This creates an **OpenAI-compatible API** at:

```
http://127.0.0.1:4000/v1
```

---

## 🔹 5. Test LiteLLM Connection

Run:

```bash
curl http://127.0.0.1:4000/v1/models
```

Expected output:

```json
{"data":[{"id":"ollama/tinyllama:latest","object":"model"}]}
```

✅ That means LiteLLM ↔ Podman Ollama is working.

---

## 🔹 6. Autogen Code

Save as `autogen_tinyllama_podman.py`:

```python
from autogen import ConversableAgent, UserProxyAgent

# LLM Configuration (connects to LiteLLM proxy → Ollama in Podman)
local_llm_config = {
    "config_list": [
        {
            "model": "ollama/tinyllama:latest",   # The lightest model
            "api_key": "not-needed",             # LiteLLM ignores this
            "base_url": "http://127.0.0.1:4000", # LiteLLM proxy endpoint
            "price": [0, 0],                     # Free since local
        }
    ],
    "cache_seed": None,
}

# Assistant agent (the AI brain)
assistant = ConversableAgent("agent", llm_config=local_llm_config)

# User proxy (represents you)
user_proxy = UserProxyAgent("user", code_execution_config=False)

# Start a conversation
res = assistant.initiate_chat(user_proxy, message="Explain recursion in one line")

print("---- Chat Result ----")
print(res)
```

---

## 🔹 7. Run the Agent

Make sure:

1. **Podman Ollama container** is running.
2. **LiteLLM** is running (`litellm --model ollama/tinyllama:latest --port 4000`).

Then run:

```bash
python autogen_tinyllama_podman.py
```

✅ You’ll get a response from **tinyllama running inside Podman** through Autogen.

---

# 📝 Summary (Human Words)

1. **Ollama in Podman** → runs models inside a container (`http://127.0.0.1:11434`).
2. **LiteLLM proxy** → converts Ollama API into OpenAI-compatible API (`http://127.0.0.1:4000/v1`).
3. **Autogen agents** → connect to LiteLLM and talk to Ollama as if it’s OpenAI.
4. Use **tinyllama** for speed and light resource usage.

------------------------------------------------------------------------------------------------------------------------------------------

👉Below is  a **multi-model setup** (tinyllama + llama3.2) so you can switch between *fast* vs *smart* inside the same Autogen run:
#Implementation
from autogen import ConversableAgent, UserProxyAgent

# LLM Configuration with multiple models
local_llm_config = {
    "config_list": [
        {
            "model": "ollama/tinyllama:latest",   # Fast + lightweight
            "api_key": "not-needed",
            "base_url": "http://127.0.0.1:4000",
            "price": [0, 0],
        },
        {
            "model": "ollama/llama3.2:latest",    # Smarter but heavier
            "api_key": "not-needed",
            "base_url": "http://127.0.0.1:4000",
            "price": [0, 0],
        }
    ],
    "cache_seed": None,
}

# Create agents for both models
fast_agent = ConversableAgent("fast_agent", llm_config={"config_list": [local_llm_config["config_list"][0]]})
smart_agent = ConversableAgent("smart_agent", llm_config={"config_list": [local_llm_config["config_list"][1]]})

# User proxy
user_proxy = UserProxyAgent("user", code_execution_config=False)

# Example: Use tinyllama for quick tasks
res1 = fast_agent.initiate_chat(user_proxy, message="Summarize recursion in one line")
print("---- Fast Agent (tinyllama) ----")
print(res1)

# Example: Use llama3.2 for deeper reasoning
res2 = smart_agent.initiate_chat(user_proxy, message="Explain recursion with an example in Python")
print("---- Smart Agent (llama3.2) ----")
print(res2)
------------------------------------------------------------------------------------------------------------------------------
Other Example:
--------------
import os
from autogen import ConversableAgent

# LiteLLM proxy URL (pointing to Ollama in Podman)
LITELLM_BASE_URL = "http://127.0.0.1:4000"

# Cathy with TinyLLaMA
cathy = ConversableAgent(
    "cathy",
    system_message="Your name is Cathy and you are a part of a duo of comedians.",
    llm_config={
        "config_list": [
            {
                "model": "ollama/tinyllama:latest",
                "temperature": 0.9,
                "api_key": "not-needed",
                "base_url": LITELLM_BASE_URL,
            }
        ]
    },
    human_input_mode="NEVER",
)

# Joe with TinyLLaMA
joe = ConversableAgent(
    "joe",
    system_message="Your name is Joe and you are a part of a duo of comedians.",
    llm_config={
        "config_list": [
            {
                "model": "ollama/tinyllama:latest",
                "temperature": 0.7,
                "api_key": "not-needed",
                "base_url": LITELLM_BASE_URL,
            }
        ]
    },
    human_input_mode="NEVER",
)

# 🎬 Make them chat
if __name__ == "__main__":
    cathy.initiate_chat(
        joe,
        message="Hey Joe, let’s make some people laugh! Start with a joke."
    )

#Note: Don't forget to start litellm proxy and check ollama is running.
