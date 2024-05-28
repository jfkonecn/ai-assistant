# AI Assistant

## Create .env file

```sh
cp .env.example .env
```

## Create config.yaml file

```sh
cp example.config.yaml config.yaml
```

## Python Info

### [Virtual Environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)

1. Create Environment

   ```sh
   python3 -m venv .venv
   ```

2. Activate Virtual Environment

   ```sh
   source .venv/bin/activate
   ```

3. Check if environment is your directory

   ```sh
   which python
   ```

4. The environment

   ```sh
   deactivate
   ```

### Update Requirements

```sh
    pip freeze > requirements.txt
```

## Ollama

1. [Install Ollama](https://ollama.com/download)
2. Pull llama3

   ```sh
   ollama pull llama3
   ```

3. Pull mxbai-embed-large

   ```sh
   ollama pull mxbai-embed-large
   ```

## Project Installation

1. Install with pip

   ```sh
   pip install -r requirements.txt
   ```
