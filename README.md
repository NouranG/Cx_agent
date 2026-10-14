# ISP Customer Support Agent

A modular, LLM-powered customer support prototype for an Internet Service Provider (ISP). It routes customer questions to specialized billing, technical-support, or knowledge-base agents, combines customer/account data with retrieved documentation where relevant, and returns a consistent response object.

## Features

- **Intent-based triage:** routes requests to `billing`, `technical`, or `knowledge`.
- **Billing support:** retrieves a customer's account and billing records before generating an answer.
- **Technical support:** combines customer network status with relevant troubleshooting documentation.
- **Knowledge-base Q&A:** retrieves relevant documentation and asks the LLM to answer using the retrieved context.
- **Documentation ingestion:** crawls configured support/documentation pages, converts HTML to cleaned Markdown, and saves it locally.
- **Semantic retrieval:** uses Hugging Face embeddings and a FAISS vector store.
- **Local LLM provider:** uses Ollama (default model: `llama3.1:8b`).
- **Consistent responses:** agents return an `AgentResponse` with success status, agent name, message, confidence, and optional data.

## Architecture

```text
Customer (terminal)
       |
       v
main.py -> APIGateway -> SupportRequest
                         |
                         v
                   ResponseEngine
                         |
                         v
                    TriageAgent
                  /      |      \
             billing  technical  knowledge
                |         |          |
             SQLite   SQLite +    FAISS retrieval
             records  retrieval       |
                \         |          /
                         LLM
                          |
                          v
                    AgentResponse
```

The knowledge preparation path is separate from interactive requests:

```text
Configured documentation sources -> crawler -> scraper -> HTML parser
                                                    |
                                                    v
                                              knowledge_base/
                                                    |
                                                    v
                                      document loading + chunking
                                                    |
                                                    v
                                           embeddings + FAISS
                                                    |
                                                    v
                                               vector_store/
```

## Repository layout

| Path | Responsibility |
|---|---|
| `main.py` | Terminal chat loop and customer ID selection |
| `core/api_gateway.py` | Validates incoming request fields and creates a `SupportRequest` |
| `core/response_engine.py` | Routes each request to the selected agent |
| `core/response.py` | Shared response model and success/failure factories |
| `agents/triage.py` | LLM-based intent routing |
| `agents/billing_agent.py` | Customer and billing lookup, then answer generation |
| `agents/technical_agent.py` | Network lookup, documentation retrieval, and troubleshooting response |
| `agents/knowledge_agent.py` | Retrieval-augmented answers from documentation |
| `database/` | SQLite access, schema, and database initialization |
| `ingestion/` | Documentation crawling, downloading, parsing, and saving |
| `llm/` | LLM provider abstraction, Ollama implementation, and prompts |
| `utils/loader.py` | Loads Markdown and PDF documents from the knowledge base |
| `utils/embeddings.py` | Builds and saves the FAISS vector index |
| `utils/retrieval.py` | Loads the index, retrieves similar documents, and formats context |
| `tests/` | Automated tests |

## Requirements

- Python **3.13 or later** (as declared in `pyproject.toml`)
- [Ollama](https://ollama.com/) running locally
- The model configured in `llm/ollama_provider.py` (default: `llama3.1:8b`)
- Python dependencies listed in `requirements.txt`
- A SQLite database initialized with the project schema
- A built FAISS index in `vector_store/` before starting the application

## Setup

### 1. Clone and install dependencies

```bash
git clone https://github.com/NouranG/Cx_agent.git
cd Cx_agent
python -m venv .venv
```

Activate the environment:

**Windows PowerShell**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Start Ollama and pull the model

Install Ollama, then run:

```bash
ollama pull llama3.1:8b
```

Make sure the Ollama service is available at `http://localhost:11434`, or update the host/model in `llm/ollama_provider.py`.

### 3. Initialize the SQLite database

```bash
python -m database.init_db
```

The application database path is `database/customers.db`. The schema is defined in `database/scheme.sql`.

### 4. Build the knowledge base and vector index

Crawl the configured documentation sources and save Markdown pages:

```bash
python -m ingestion.ingest
```

Then load the saved documents, split them into chunks, and build the FAISS index:

```bash
python -c "from langchain_text_splitters import RecursiveCharacterTextSplitter; from utils.loader import KnowledgeLoader; from utils.embeddings import EmbeddingBuilder; docs=KnowledgeLoader().load_documents(); chunks=RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=120).split_documents(docs); EmbeddingBuilder().build(chunks)"
```

The embedding model `BAAI/bge-small-en-v1.5` is downloaded on first use. The index is saved under `vector_store/`.

> The first-time ingestion/indexing step requires network access. If crawling fails because a source changes its website structure or rate-limits requests, inspect the failed URL and retry; do not assume every configured page was ingested.

### 5. Run the terminal assistant

```bash
python main.py
```

The current demo uses customer ID `1001`. Enter a support question at the prompt; type `exit` to quit.

Example questions:

- `How much is my bill and when is it due?`
- `Why is my internet down?`
- `How do I restart my router?`

Answers depend on the initialized sample data, the built knowledge index, and the local LLM being available.

## Tests

Run the automated test suite from the repository root:

```bash
pytest -q
```

Unit tests should use mocks for LLM calls, retrieval, and network requests so the core test suite does not require a running Ollama server or live documentation websites. Tests that intentionally exercise the full local stack should be run separately and documented as integration tests.

## Current scope and limitations

- This is a local prototype with a terminal interface, not a deployed web API.
- The gateway validates basic request fields; production use would also need stronger request validation, authentication, authorization, and rate limiting.
- The LLM router falls back to the knowledge agent if it returns an unexpected label.
- Retrieval quality depends on the source documents and index built locally.
- The vector store is loaded at import time through the singleton module, so it must exist before importing the agents that use retrieval.
- Billing and technical answers depend on customer data being present and consistent with the database schema.

## Possible next steps

- Add integration tests for the full gateway-to-agent flow and database behavior.
- Evaluate triage accuracy on a labeled set of customer queries.
- Measure retrieval quality (for example, Recall@k / MRR) and answer faithfulness against source documents.
- Add structured logging, timeouts/retries, and clear handling for Ollama or vector-store failures.
- Add a web API, authentication, and safe authorization checks before exposing customer data.
