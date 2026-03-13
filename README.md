# Desafio MBA Engenharia de Software com IA - Full Cycle

1. **Criar e ativar um ambiente virtual (`venv`):**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

2. **Instalar as dependências:**

   **A partir do `requirements.txt`:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar as variáveis de ambiente:**

   - Duplique o arquivo `.env.example` e renomeie para `.env`
   - Abra o arquivo `.env` e substitua os valores pelas suas chaves de API reais obtidas

4. **Subir o banco de dados**

    - Na raíz do projeto rode o comando: docker-compose up -d

5. **Rodar o script para ingestao do PDF no banco de dados**

    - Abrir a pasta src (cd src)
    - Rodar o comando: python ingest.py