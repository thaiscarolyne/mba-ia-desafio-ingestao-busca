import os

from search import search_prompt
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables import RunnablePassthrough, RunnableWithMessageHistory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_postgres import PGVector
from dotenv import load_dotenv

load_dotenv()

# --- Configuração do Banco de Dados (Retriever) ---
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True,
)
retriever = store.as_retriever(search_kwargs={"k": 10})

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

chat_model = ChatOpenAI(model="gpt-5-nano", temperature=0.9)

session_store = {}

def get_session_history(session_id: str):
    if session_id not in session_store:
        session_store[session_id] = InMemoryChatMessageHistory()
    return session_store[session_id]

def main():
    prompt = search_prompt()

    # 1. Pega a 'question'
    # 2. Passa pelo retriever e salva em 'pdf_context'
    # 3. Mantém a 'question' e 'contexto' original para o próximo passo
    rag_chain = (
        {
            # Pegamos apenas a string da 'question' para o retriever
            "pdf_context": (lambda x: x["question"]) | retriever | format_docs, 
            # Apenas passa adiante a question e o contexto
            "question": lambda x: x["question"],
            "contexto": lambda x: x["contexto"]
        }
        | prompt
        | chat_model
    )

    # Envolvemos a RAG chain com a memória
    full_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="question",
        history_messages_key="contexto",
    )

    config = {"configurable": {"session_id": "session-chat-rag"}}

    print("\n" + "="*50)
    print("SISTEMA RAG PRONTO! (Digite 'sair' para encerrar)")
    print("="*50 + "\n")

    while True:
        # 1. Pega a entrada do usuário
        user_input = input("Você: ")

        # 2. Verifica se o usuário quer sair
        if user_input.lower() in ["sair", "exit", "quit", "parar"]:
            print("Encerrando chat. Até logo!")
            break

        # 3. Se a entrada estiver vazia, ignora
        if not user_input.strip():
            continue

        try:
            # 4. Envia para a chain (agora dentro do loop)
            response = full_chain.invoke({"question": user_input}, config=config)
            
            # 5. Exibe a resposta do assistente
            print(f"\nAssistant: {response.content}")
            print("-" * 30 + "\n")
            
        except Exception as e:
            print(f"\n[ERRO]: Ocorreu um problema ao processar sua pergunta: {e}\n")

if __name__ == "__main__":
    main()