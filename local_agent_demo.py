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
    categories = st_tags(
        label="Enter Categories:",
        text="Press enter to add more",
        value=["Food", "Travel", "Business", "Others", "Miscellaneous"],
        suggestions=["Food", "Travel", "Business", "Others", "Miscellaneous"]
    )
    file = st.file_uploader("Upload CSV file", type=["csv"])
    if file is not None:
        csv_data = file.getvalue().decode("utf-8")
        prompt = f"Categories the provided records into {','.join(categories)} and return the output in JSON format with complete transaction records.\n" + " " + csv_data

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