"""
Script para fazer push de prompts otimizados ao LangSmith Prompt Hub.

Este script:
1. Lê os prompts otimizados de prompts/bug_to_user_story_v2.yml
2. Valida os prompts
3. Faz push PÚBLICO para o LangSmith Hub
4. Adiciona metadados (tags, descrição, técnicas utilizadas)

SIMPLIFICADO: Código mais limpo e direto ao ponto.
"""

import os
import sys
from dotenv import load_dotenv
from langchain import hub
from langchain_core.prompts import ChatPromptTemplate
from utils import load_yaml, check_env_vars, print_section_header

load_dotenv()


def push_prompt_to_langsmith(prompt_name: str, prompt_data: dict) -> bool:
    try:
        messages = []

        # Adiciona system_prompt (string)
        if "system_prompt" in prompt_data:
            messages.append(("system", prompt_data["system_prompt"]))

        # Adiciona user_prompt (string)
        if "user_prompt" in prompt_data:
            messages.append(("user", prompt_data["user_prompt"]))

        prompt = ChatPromptTemplate.from_messages(messages)

        hub.push(f"{prompt_name}", prompt)

        print(f"Prompt '{prompt_name}' publicado com sucesso!")
        return True

    except Exception as e:
        print(f"Erro ao publicar '{prompt_name}': {e}")
        return False


def validate_prompt(prompt_data: dict) -> tuple[bool, list]:
    errors = []

    # --- validar campo system_prompt ---
    if "system_prompt" not in prompt_data:
        errors.append("Campo 'system_prompt' ausente.")
    else:
        system_val = prompt_data["system_prompt"]
        if not isinstance(system_val, str) or not system_val.strip():
            errors.append("Campo 'system_prompt' deve ser uma string não vazia.")

    # --- validar campo user_prompt ---
    if "user_prompt" not in prompt_data:
        errors.append("Campo 'user_prompt' ausente.")
    else:
        user_val = prompt_data["user_prompt"]
        if not isinstance(user_val, str) or not user_val.strip():
            errors.append("Campo 'user_prompt' deve ser uma string não vazia.")

    return (len(errors) == 0, errors)

def main():
    print_section_header("PUSH DE PROMPTS OTIMIZADOS")

    required_vars = ["LANGSMITH_API_KEY"]
    if not check_env_vars(required_vars):
        return 1

    prompt_file = "prompts/bug_to_user_story_v2.yml"

    if not os.path.exists(prompt_file):
        print(f"Arquivo não encontrado: {prompt_file}")
        return 1

    print(f"Carregando: {prompt_file}")
    prompt_data = load_yaml(prompt_file)

    if isinstance(prompt_data, dict) and len(prompt_data) == 1:
        root_key = list(prompt_data.keys())[0]
        prompt_name = root_key
        prompt_data = prompt_data[root_key]
    else:
        prompt_name = prompt_data.get("name", "prompt_sem_nome")

    print("Validando prompt...")
    is_valid, errors = validate_prompt(prompt_data)

    if not is_valid:
        print("Erros na validação do prompt:")
        for err in errors:
            print(f" - {err}")
        return 1

    print("Enviando para LangSmith Hub...")
    success = push_prompt_to_langsmith(prompt_name, prompt_data)

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
