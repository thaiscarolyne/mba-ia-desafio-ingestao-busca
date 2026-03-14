from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

def search_prompt():
    return ChatPromptTemplate.from_messages([
    ("system", """REGRAS:
- Responda somente com base no CONTEXTO {pdf_context}
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."""),
    MessagesPlaceholder(variable_name="contexto"),
    ("human", "{question}"),
])