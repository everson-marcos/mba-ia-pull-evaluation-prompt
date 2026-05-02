# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Este projeto tem como objetivo construir um pipeline completo para **baixar, otimizar, publicar e avaliar prompts** utilizando LangChain e LangSmith.  
O sistema foi projetado para identificar prompts de baixa qualidade, refatorá-los usando técnicas avançadas de Prompt Engineering e garantir sua aprovação através de métricas customizadas.

O fluxo final garante que cada prompt otimizado atinja **nota mínima de 0.9** em todas as métricas avaliadas.

---

## Como o projeto funciona

O pipeline é dividido em quatro etapas principais:

### 1. 📥 Pull de Prompts (src/pull_prompts.py)
- Conecta ao **LangSmith Prompt Hub**
- Baixa os prompts originais (geralmente versões ruins ou desatualizadas)
- Salva em `prompts/raw_prompts.yml`

### 2. 🛠️ Otimização manual dos prompts
- Você edita os prompts baixados
- Cria uma nova versão otimizada, ex:
  - `prompts/bug_to_user_story_v2.yml`
- Aplica técnicas como:
  - Few-Shot Learning
  - Chain of Thought
  - Role Prompting
  - Skeleton of Thought
  - Tree of Thought
  - ReAct
- Documenta no README as técnicas utilizadas e as razões

### 3. 📤 Push de Prompts Otimizados (src/push_prompts.py)
- Publica a nova versão no **LangSmith Prompt Hub**

### 4. 🧪 Avaliação automática (src/evaluate.py)
- Executa testes com dataset de exemplos
- Gera métricas:
  - F1-Score
  - Clarity
  - Precision
  - Helpfulness
  - Correctness
- Classifica como:
  - **APROVADO** (≥ 0.9)
  - **REPROVADO** (< 0.9)

---

## Exemplo no CLI

```bash
# 1. Fazer pull dos prompts ruins do LangSmith
python src/pull_prompts.py

# 2. Avaliar qualidade inicial
python src/evaluate.py

# (resultado: reprovação)
================================
Prompt: support_bot_v1
- Helpfulness: 0.45
- Correctness: 0.52
- F1-Score: 0.48
- Clarity: 0.50
- Precision: 0.46
Status: FALHOU
================================

# 3. Depois de otimizar manualmente, enviar nova versão
python src/push_prompts.py

# 4. Avaliar novamente
python src/evaluate.py

================================
Prompt: support_bot_v2
- Helpfulness: 0.94
- Correctness: 0.96
- F1-Score: 0.93
- Clarity: 0.95
- Precision: 0.92
Status: APROVADO ✓
================================