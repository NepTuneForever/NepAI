# NepAI

Local chat assistant in Python using `Ollama` with a pre-trained model.

## How it works

- `minhaia.py` sends your messages to `Ollama`
- `Ollama` runs the local model on your PC
- `knowledge/conhecimento.txt` stores persistent knowledge

## Requirements

- Python 3
- Ollama installed on Windows
- A downloaded model, for example:

```powershell
ollama pull llama3.1:8b
```

## How to run

```powershell
cd C:\Users\Windows\Documents\GitHub\minhaia
python minhaia.py
```

## Chat commands

- `sair`
- `limpar`
- `ajuda`
- `ver conhecimento`
- `ensinar: <text>`

## How to teach new knowledge

Example:

```text
ensinar: The transmission helps control how power is delivered to the wheels.
```

This is saved to `knowledge/conhecimento.txt` and remains available after you close the chat.

## Project structure

- `minhaia.py`: main chat script
- `knowledge/conhecimento.txt`: persistent knowledge base
- `.gitignore`: files that should not be committed
