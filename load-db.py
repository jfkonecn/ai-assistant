# https://ollama.com/blog/embedding-models
# https://docs.trychroma.com/guides
# type: ignore

import os
from collections.abc import Callable
from warnings import warn

import chromadb
import ollama
import PyPDF2
import yaml
from dotenv import load_dotenv

WriteCollection = Callable[[int, str], None]


def writePdf(filePath: str, writeToCollection: WriteCollection):
    pdf_file = open(filePath, "rb")
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    totalPages = len(pdf_reader.pages)
    all_text = ""
    for page_num in range(totalPages):
        print(f"processing page #{page_num} of {totalPages} for {filePath}")
        page = pdf_reader.pages[page_num]
        all_text += f"Start of Page {page_num} of {totalPages}"
        all_text += f"{page.extract_text()}\n"
        all_text += f"End of Page {page_num} of {totalPages}"
    writeToCollection(0, all_text)


load_dotenv(".env")

dbPath = os.environ.get("DB_PATH")
configPath = os.environ.get("CONFIG_PATH")

client = chromadb.PersistentClient(path=dbPath)

with open(configPath, "r") as f:
    data = yaml.load(f, Loader=yaml.SafeLoader)

for collectionName, dataPath in data["paths"].items():
    collection = client.get_or_create_collection(name=collectionName)
    for root, dirs, files in os.walk(os.path.expanduser(dataPath)):
        for file in files:
            file_path: str = os.path.join(root, file)
            print(f"processing {file_path}...")

            def writeCollection(pageNumber: int, contents: str):
                response = ollama.embeddings(model="mxbai-embed-large", prompt=contents)
                embedding = response["embedding"]
                if len(embedding) == 0:
                    warn(
                        f"embeddings are empty for {file_path}#{pageNumber} skipping..."
                    )
                else:
                    collection.add(
                        ids=[f"{file_path}#{pageNumber}"],
                        embeddings=[embedding],
                        documents=[str.upper(contents)],
                    )

            if file.endswith(".pdf"):
                writePdf(file_path, writeCollection)


# # store each document in a vector embedding database
# for i, d in enumerate(documents):
# response = ollama.embeddings(model="mxbai-embed-large", prompt=d)
# embedding = response["embedding"]
# collection.add(ids=[str(i)], embeddings=[embedding], documents=[d])
