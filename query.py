# an example prompt
# type: ignore
import os
from logging import warn

import chromadb
import ollama
from dotenv import load_dotenv
from rich.console import Console
from rich.markdown import Markdown

console = Console()


def print_md(x: str):
    console.log(Markdown(x))


load_dotenv(".env")
configPath = os.environ.get("CONFIG_PATH")


dbPath = os.environ.get("DB_PATH")

# with open(configPath, "r") as f:
# data = yaml.load(f, Loader=yaml.SafeLoader)

# options = list(data["paths"].keys())
client = chromadb.PersistentClient(path=dbPath)
options = list(map(lambda x: x.name, client.list_collections()))
pickedOption: str = None

while pickedOption is None:
    for i, option in enumerate(options):
        print(f"{i + 1}. {option}")
    print("q: quit")
    answer = input("> ")
    if answer == "q":
        exit(0)
    try:
        pickedIdx = int(answer) - 1
        if pickedIdx < 0 or pickedIdx >= len(options):
            raise Exception("out of range")
        else:
            pickedOption = options[pickedIdx]
    except Exception:
        print(f"invalid option {answer}")

client = chromadb.PersistentClient(path=dbPath)
collection = client.get_collection(name=pickedOption)
messages = []
keywords = []


def send_message_to_llm(message):
    messages.append({"role": "user", "content": message})

    # output = ollama.generate(
    # model="llama3",
    # # prompt=f"Using this data: {data}. Respond to this prompt: {prompt}"
    # prompt=ragPrompt,
    # )
    output = ollama.chat(model="llama3", messages=messages)

    answer = "## Summary\n\n"
    botAnswer = output["message"]

    messages.append(botAnswer)

    answer += botAnswer["content"]

    print_md(answer)


def search_text(prompt: str):
    # generate an embedding for the prompt and retrieve the most relevant doc
    response = ollama.embeddings(prompt=prompt, model="mxbai-embed-large")
    where_document = None
    if len(keywords) > 1:
        where_document = {
            "$or": list(
                map(lambda keyword: {"$contains": str.upper(keyword)}, keywords)
            )
        }
    elif len(keywords) == 1:
        where_document = {"$contains": str.upper(keywords[0])}

    results = collection.query(
        query_embeddings=[response["embedding"]],
        # n_results=10,
        where_document=where_document,
        # where_document=where_document,
    )
    # data = str.join("\n", results["documents"][0])

    # print(data)

    pdfContent = ""
    for i, doc in enumerate(results["documents"][0]):
        # pdfContent += f"## {results['ids'][0][i]}\n\n"
        pdfContent += f"{doc}\n\n"

    ragPrompt = f"""
You are an expert in finding information. You will be provided with sources delimited by triple quotes and a question. Your task is to answer the question using only the provided document and to cite the passage(s) of the document used to answer the question. If the document does not contain the information needed to answer this question then simply write: "Insufficient information." If an answer to the question is provided, it MUST be annotated with a citation. Use the following format for to cite relevant passages ({{"citation": …}}).
    \"\"\"{pdfContent}\"\"\"
    Question: {prompt}
    """
    send_message_to_llm(ragPrompt)


prompt = ""


def printOptions():
    print("/? for help")
    print("/bye to quit")
    print("To add keywords:")
    print("/keywords <word> <word>")
    print("To clear keywords:")
    print("/clear keywords")


printOptions()

while prompt != "/bye":
    joined_keywords = ""
    if len(keywords) > 0:
        joined = str.join(",", keywords)
        joined_keywords = f"({joined})"
    prompt = input(f"{joined_keywords}>>> ")
    if prompt[0] != "/":
        search_text(prompt)
    elif prompt == "/clear keywords":
        keywords = []
    elif prompt.startswith("/keywords "):
        keywords.extend(prompt.split(" ")[1:])
    elif prompt != "/bye":
        printOptions()
