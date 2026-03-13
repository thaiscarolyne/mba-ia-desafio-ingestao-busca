import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")
loader = PyPDFLoader(PDF_PATH)
docs = loader.load()
console = Console()

def ingest_pdf():
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_documents(docs)
    # Cabeçalho do resumo
    console.print(Panel(f"Processamento concluído: [bold green]{len(chunks)}[/bold green] chunks gerados."), style="bold blue")

    for i, chunk in enumerate(chunks):
        # Criando o cabeçalho de cada chunk
        header = Text(f" Chunk {i + 1} ", style="bold black on cyan")
        
        # Conteúdo com destaque para metadados
        content = chunk.page_content.replace("\n", " ") # Opcional: limpa quebras de linha extras
        metadata = f"\n\n[dim cyan]Fonte: {chunk.metadata.get('source')} | Página: {chunk.metadata.get('page') + 1}[/dim cyan]"
        
        print(header)
        console.print(content)
        console.print(metadata)
        console.print("-" * 50) # Separador visual simples

    ids = [f"doc-{i}" for i in range(len(chunks))]

    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_MODEL","text-embedding-3-small"))

    store = PGVector(
    embeddings=embeddings,
    collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True,)

    store.add_documents(documents=chunks, ids=ids)


if __name__ == "__main__":
    ingest_pdf()