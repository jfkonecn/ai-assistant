# https://ollama.com/blog/embedding-models
# https://docs.trychroma.com/guides

import os

import chromadb
import ollama
import yaml
from dotenv import load_dotenv

load_dotenv(".env")

dbPath = os.environ.get("DB_PATH")
configPath = os.environ.get("CONFIG_PATH")

with open(configPath, "r") as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)

for collectionName, dataPath in data["paths"].items():
    for root, dirs, files in os.walk(os.path.expanduser(dataPath)):
        print(root)
        for file in files:
            if file.endswith(".pdf"):
                pdf_file_path = os.path.join(root, file)
                # Do something with the PDF file here, e.g.:
                print(f"Processing {pdf_file_path}...")


# documents = [
# "Llamas are members of the camelid family meaning they're pretty closely related to vicuñas and camels",
# "Llamas were first domesticated and used as pack animals 4,000 to 5,000 years ago in the Peruvian highlands",
# "Llamas can grow as much as 6 feet tall though the average llama between 5 feet 6 inches and 5 feet 9 inches tall",
# "Llamas weigh between 280 and 450 pounds and can carry 25 to 30 percent of their body weight",
# "Llamas are vegetarians and have very efficient digestive systems",
# "Llamas live to be about 20 years old, though some only live for 15 years and others live to be 30 years old",
# ]

# client = chromadb.PersistentClient(path=dbPath)
# collection = client.create_collection(name="docs")

# # store each document in a vector embedding database
# for i, d in enumerate(documents):
# response = ollama.embeddings(model="mxbai-embed-large", prompt=d)
# embedding = response["embedding"]
# collection.add(ids=[str(i)], embeddings=[embedding], documents=[d])
