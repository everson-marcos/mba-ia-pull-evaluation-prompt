"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

PROMPT_NAME = "leonanluppi/bug_to_user_story_v1"
OUTPUT_FILE = Path("prompts/bug_to_user_story_v1.yml")


def pull_prompts_from_langsmith():
    print_section_header(f"Baixando prompt: {PROMPT_NAME}")

    try:
        prompt = hub.pull(PROMPT_NAME)
    except Exception as e:
        print(f"Erro ao fazer pull do prompt: {e}")
        sys.exit(1)

    # Serialização nativa e consistente
    messages = []
    for msg in prompt.messages:
        msg_dict = msg.to_dict() if hasattr(msg, "to_dict") else {"type": str(msg)}
        messages.append(msg_dict)

    return {
        "name": PROMPT_NAME,
        "messages": messages,
    }


def main():
    """Função principal"""
    check_env_vars(["LANGSMITH_API_KEY"])

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    prompt_data = pull_prompts_from_langsmith()
    save_yaml(prompt_data, OUTPUT_FILE) 

    print_section_header("Pull concluído! Arquivo salvo em:")
    print(f"{OUTPUT_FILE}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
