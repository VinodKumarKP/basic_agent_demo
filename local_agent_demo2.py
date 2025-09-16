import json

import requests
import streamlit as st
from streamlit_tags import st_tags


class LocalAIClient:
    """Client for interacting with various local AI models"""

    def __init__(self, base_url: str = "http://localhost:11434", model_type: str = "ollama"):
        self.base_url = base_url.rstrip('/')
        self.model_type = model_type.lower()
        self.session = requests.Session()

    def ollama_chat(self, model: str, prompt: str, system_prompt: str = None) -> str:
        """Interact with Ollama API"""
        url = f"{self.base_url}/api/generate"

        data = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }

        if system_prompt:
            data["system"] = system_prompt

        try:
            st.write(f"Sending request to Ollama using url: {url}")
            st.json(f"{json.dumps(data)}")
            response = self.session.post(url, json=data, timeout=120)
            # response.raise_for_status()
            return response.json().get("response", "No response received")
        except requests.exceptions.RequestException as e:
            return f"Error communicating with Ollama: {e}"

client = LocalAIClient(
    base_url="http://3.138.118.212:11434",
    model_type="ollama"
)

with open("transaction.csv") as f:
    csv_data = f.read()


with st.container():

    prompt = st.text_input("Enter your prompt here")

    if prompt:
        with st.spinner('Generating response...'):
            response = client.ollama_chat(
                model="llama3.2",
                prompt=prompt,
                system_prompt="""
                You are an AI assistant that helps people.
                """

            )

            st.write(response)