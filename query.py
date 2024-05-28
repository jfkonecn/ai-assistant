# an example prompt
import os

import chromadb
import ollama
from dotenv import load_dotenv

load_dotenv(".env")

dbPath = os.environ.get("DB_PATH")

client = chromadb.PersistentClient(path=dbPath)
collection = client.get_collection(name="docs")

prompt = "What animals are llamas related to?"

# generate an embedding for the prompt and retrieve the most relevant doc
response = ollama.embeddings(prompt=prompt, model="mxbai-embed-large")
results = collection.query(query_embeddings=[response["embedding"]], n_results=1)
data = results["documents"][0][0]

output = ollama.generate(
    model="llama3", prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
)

print(data)
print(output["response"])
