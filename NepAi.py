import json
import os
import urllib.error
import urllib.request


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")
KNOWLEDGE_FILE = os.path.join(KNOWLEDGE_DIR, "conhecimento.txt")
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.1:8b"
BASE_SYSTEM_PROMPT = (
    "Voce e um assistente util, direto e natural. "
    "Responda sempre em portugues do Brasil, a menos que o usuario peca outro idioma. "
    "Quando houver conhecimento fornecido pelo usuario, priorize esse conhecimento."
)


def ensure_structure():
    os.makedirs(KNOWLEDGE_DIR, exist_ok=True)

    if not os.path.exists(KNOWLEDGE_FILE):
        with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as file:
            file.write(
                "Um carro e um veiculo usado para transportar pessoas.\n"
                "Um carro normalmente tem rodas, motor, volante, freios e bancos.\n"
                "O volante serve para controlar a direcao do carro.\n"
                "Os freios servem para diminuir a velocidade ou parar o carro.\n"
                "O motor fornece energia para movimentar o carro.\n"
            )


def load_knowledge():
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
        return file.read().strip()


def build_system_prompt():
    knowledge = load_knowledge()

    if not knowledge:
        return BASE_SYSTEM_PROMPT

    return (
        f"{BASE_SYSTEM_PROMPT}\n\n"
        "Conhecimento salvo pelo usuario:\n"
        f"{knowledge}"
    )


def append_knowledge(text):
    with open(KNOWLEDGE_FILE, "a", encoding="utf-8") as file:
        if os.path.getsize(KNOWLEDGE_FILE) > 0:
            file.write("\n")
        file.write(text.strip())


def chat_with_model(messages):
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
    }

    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(request, timeout=300) as response:
        body = response.read().decode("utf-8")
        parsed = json.loads(body)
        return parsed["message"]["content"].strip()


def create_base_messages():
    return [{"role": "system", "content": build_system_prompt()}]


def print_help():
    print("Comandos:")
    print("  sair                       -> fecha o chat")
    print("  limpar                     -> apaga o historico da conversa atual")
    print("  ajuda                      -> mostra esta ajuda")
    print("  ensinar: <texto>           -> salva conhecimento para proximas conversas")
    print("  ver conhecimento           -> mostra o arquivo de conhecimento atual")


def run_chat():
    ensure_structure()
    messages = create_base_messages()

    print(f"Modelo: {MODEL}")
    print("Digite sua mensagem.")
    print("Use 'sair' para fechar.")
    print("Use 'ensinar: ...' para salvar conhecimento permanente.")

    while True:
        user_input = input("\nVoce: ").strip()

        if not user_input:
            continue

        command = user_input.lower()

        if command == "sair":
            print("IA: Encerrando.")
            break

        if command == "ajuda":
            print_help()
            continue

        if command == "limpar":
            messages = create_base_messages()
            print("IA: Historico limpo.")
            continue

        if command == "ver conhecimento":
            print("IA:")
            print(load_knowledge() or "[vazio]")
            continue

        if command.startswith("ensinar:"):
            new_knowledge = user_input[len("ensinar:"):].strip()

            if not new_knowledge:
                print("IA: Escreva algo depois de 'ensinar:'.")
                continue

            append_knowledge(new_knowledge)
            messages = create_base_messages()
            print("IA: Conhecimento salvo. Vou usar isso nas proximas respostas.")
            continue

        messages.append({"role": "user", "content": user_input})

        try:
            reply = chat_with_model(messages)
        except urllib.error.URLError:
            print("IA: Nao consegui conectar ao Ollama em http://localhost:11434.")
            print("IA: Verifique se o Ollama esta aberto no Windows.")
            continue
        except KeyError:
            print("IA: Recebi uma resposta inesperada do Ollama.")
            continue
        except Exception as error:
            print(f"IA: Ocorreu um erro: {error}")
            continue

        messages.append({"role": "assistant", "content": reply})
        print(f"IA: {reply}")


if __name__ == "__main__":
    run_chat()
