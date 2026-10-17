# Enterprise Corrective RAG

A locally runnable Retrieval-Augmented Generation (RAG) project that
improves answer reliability by evaluating retrieved context before
generating a response. Instead of blindly trusting the top search
results, the pipeline checks whether retrieved information is relevant,
then uses a corrective path when the evidence is weak or ambiguous.

The project is inspired by the Corrective RAG (CRAG) approach and is
being developed as a simplified, understandable implementation for
enterprise knowledge such as reimbursement policies, HR guidance, IT
procedures, onboarding documentation, and internal FAQs.

## Table of Contents

-   [Problem Statement](#problem-statement)
-   [Solution](#solution)
-   [Architecture](#architecture)
-   [How the Pipeline Works](#how-the-pipeline-works)
-   [Key Features](#key-features)
-   [Technology Stack](#technology-stack)
-   [Project Structure](#project-structure)
-   [Prerequisites](#prerequisites)
-   [Installation and Setup](#installation-and-setup)
-   [Run the Project](#run-the-project)
-   [Add Your Own Documents](#add-your-own-documents)
-   [Testing](#testing)
-   [Configuration](#configuration)
-   [Design Decisions](#design-decisions)
-   [Current Scope and Roadmap](#current-scope-and-roadmap)
-   [Troubleshooting](#troubleshooting)
-   [Security Notes](#security-notes)
-   [Contributing](#contributing)
-   [License](#license)

## Problem Statement

Traditional RAG systems retrieve document chunks using semantic
similarity and pass them directly to a language model. This can produce
unreliable answers when:

-   The retrieved chunks are only loosely related to the user's
    question.
-   Relevant information is missing from the indexed documents.
-   Search results contain conflicting, incomplete, or ambiguous
    evidence.
-   The model generates an answer that goes beyond the available
    context.

For enterprise use cases, unsupported answers can be particularly
problematic. A system answering questions about reimbursement, leave, HR
policy, or IT processes should distinguish between evidence it can trust
and information that needs further retrieval.

## Solution

Enterprise Corrective RAG adds a retrieval-evaluation stage before
answer generation.

1.  Load source documents and extract their text.
2.  Split the text into overlapping chunks.
3.  Generate embeddings and store the chunks in a persistent Chroma
    vector store.
4.  Retrieve candidate chunks for a user query.
5.  Grade the retrieved evidence as **CORRECT**, **AMBIGUOUS**, or
    **INCORRECT**.
6.  Use the evaluation to decide whether to proceed with the available
    context or enter a correction path, such as refining the query and
    retrieving again.
7.  Generate an answer grounded in the available evidence.

The goal is to improve relevance and reduce unsupported answers---not to
guarantee that every generated response is correct. The system should
communicate when its indexed knowledge is insufficient.

## Architecture

``` mermaid
flowchart TD
    A[PDF / Knowledge Documents] --> B[Document Loader]
    B --> C[Text Chunker]
    C --> D[Embedding Model]
    D --> E[(Persistent Chroma Vector Store)]

    Q[User Query] --> R[Semantic Retrieval]
    E --> R
    R --> G[Retrieval Grader]

    G -->|CORRECT| K[Use Retrieved Context]
    G -->|AMBIGUOUS| X[Correction / Refined Retrieval]
    G -->|INCORRECT| X

    X --> R
    K --> L[Local LLM]
    L --> O[Grounded Answer]
```

### Architecture components

  -----------------------------------------------------------------------
  Component                           Responsibility
  ----------------------------------- -----------------------------------
  Document loader                     Reads supported source files and
                                      extracts text.

  Chunker                             Splits long documents into
                                      manageable, overlapping text
                                      segments.

  Embedding model                     Converts text into vectors for
                                      semantic retrieval.

  Chroma vector store                 Persists document chunks and their
                                      embeddings for search.

  Retriever                           Finds candidate chunks relevant to
                                      a user's question.

  Retrieval grader                    Evaluates whether the retrieved
                                      evidence is useful for answering
                                      the query.

  Correction path                     Refines retrieval when the evidence
                                      is ambiguous or insufficient.

  Local language model                Generates a response using the
                                      selected context.
  -----------------------------------------------------------------------

> **Implementation note:** The architecture describes the intended
> Corrective RAG flow. External web search, a complete agent workflow,
> and user-interface features should only be considered available once
> they have been implemented and configured in the project.

## How the Pipeline Works

### 1. Ingestion

Documents are loaded and converted into text. The extracted content is
split into chunks so that retrieval can select relevant passages instead
of passing an entire document to the language model.

### 2. Embeddings and indexing

The embedding model converts chunks into numerical vectors. Chroma
stores the vectors and associated text so that the index can be reused
between runs.

### 3. Retrieval

A user query is embedded and compared with indexed chunks. The retriever
returns candidate passages that may contain the information needed to
answer the question.

### 4. Retrieval grading

The grader assesses the retrieved evidence in relation to the question:

-   **CORRECT:** The retrieved context appears relevant enough to
    continue.
-   **AMBIGUOUS:** The evidence may be incomplete or only partially
    relevant.
-   **INCORRECT:** The retrieved context does not adequately support the
    question.

These are retrieval-quality decisions, not proof that every statement in
a source document is factually true.

### 5. Correction and generation

If the retrieved evidence is weak, the corrective path can refine the
query and attempt retrieval again. The selected evidence is then
supplied to the local language model to produce a context-grounded
answer.

## Key Features

-   **Local-first model workflow:** Uses Ollama-hosted models for
    embeddings and generation.
-   **PDF ingestion:** Extracts text from PDF documents.
-   **Chunk-based indexing:** Uses configurable chunk size and overlap.
-   **Persistent vector storage:** Stores embeddings in Chroma for
    reuse.
-   **Retrieval-quality evaluation:** Classifies retrieved evidence as
    correct, ambiguous, or incorrect.
-   **Testable modules:** Loader, chunker, vector store, and retrieval
    grader can be validated independently.
-   **Extensible design:** Separates ingestion, retrieval, correction,
    and generation responsibilities.

## Technology Stack

  -----------------------------------------------------------------------
  Technology                          Purpose
  ----------------------------------- -----------------------------------
  Python                              Core implementation

  LangChain                           Document processing and model
                                      integration

  Ollama                              Local model runtime

  `nomic-embed-text:latest`           Embedding model used in the
                                      development setup

  `qwen3:8b`                          Local generation model used in the
                                      development setup

  ChromaDB                            Persistent vector database

  PyPDF                               PDF text extraction

  Pytest                              Automated tests
  -----------------------------------------------------------------------

Model names reflect the development setup and can be changed to other
compatible Ollama models.

## Project Structure

The repository has been organized by responsibility. The exact files may
evolve as the project develops.

``` text
enterprise-corrective-rag/
├── app/
│   ├── ingestion/
│   │   ├── loader.py
│   │   └── embedder.py
│   ├── retrieval/
│   ├── correction/
│   └── generation/
├── data/
│   └── reimbursement/
│       └── Sample_Financial_Reimbursement_Policy.pdf
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

Some folders may contain additional modules or may still be under
development. Update this tree to match the files actually committed to
GitHub.

## Prerequisites

Install the following before running the project:

-   Python 3.10 or a compatible Python version supported by the
    installed dependencies.
-   Git.
-   Ollama installed and running locally.
-   Enough RAM and disk space for the selected local models and vector
    index.

Check the installed tools:

``` bash
python --version
git --version
ollama --version
```

## Installation and Setup

### 1. Clone the repository

``` bash
git clone https://github.com/BitsnBytes99/enterprise-corrective-rag.git
cd enterprise-corrective-rag
```

### 2. Create and activate a virtual environment

**Windows --- PowerShell**

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Windows --- Git Bash**

``` bash
python -m venv .venv
source .venv/Scripts/activate
```

**Linux / macOS**

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Pull the local models

``` bash
ollama pull nomic-embed-text
ollama pull qwen3:8b
```

Ensure Ollama is running before executing ingestion, retrieval, or
generation code. If you change the embedding model after creating the
vector index, rebuild the index so that stored and query embeddings are
compatible.

### 5. Configure environment variables

If the project uses environment variables, create a local `.env` file
from the example:

``` bash
cp .env.example .env
```

On Windows, you can also copy the file using File Explorer. Add only the
variables actually used by your implementation. Do not commit `.env` or
secret values.

If `.env.example` does not exist in the repository yet, create one
containing variable names and safe placeholder values---never real
credentials.

## Run the Project

Run commands from the repository root with the virtual environment
activated.

The current project is organized into Python modules and tests. Use the
entry point that exists in the checked-out version of the repository; do
not assume an API server or web UI is available unless its startup
module has been added.

To inspect the available files:

``` bash
git status
```

To run the test suite:

``` bash
python -m pytest -v
```

If the project later exposes a FastAPI application, document its actual
module path and start command here (for example,
`uvicorn package.module:app --reload`). Replace that example with the
real entry point before advertising the API as runnable.

## Add Your Own Documents

1.  Place the source document in the project's configured data
    directory, or use the upload mechanism if one has been implemented.
2.  Run the ingestion process to extract the text and split it into
    chunks.
3.  Generate embeddings with the configured embedding model.
4.  Store the chunks and vectors in the persistent Chroma collection.
5.  Ask a question that can be answered from the indexed content.
6.  Inspect the retrieved passages and grader result when debugging
    answer quality.

The exact ingestion command depends on the project's current entry
point. Avoid adding confidential company documents to a public
repository.

## Testing

Run all tests:

``` bash
python -m pytest -v
```

Run an individual test module, if present:

``` bash
python -m pytest tests/test_loader.py -v
python -m pytest tests/test_chunker.py -v
python -m pytest tests/test_vector_store.py -v
python -m pytest tests/test_retrieval_grader.py -v
```

The test modules are intended to validate the document loader, chunking,
vector-store operations, and retrieval grading. Test filenames may
differ in your current checkout; use `pytest --collect-only -q` to list
the tests that are available.

## Configuration

Important settings to keep consistent across the pipeline include:

-   **Chunk size:** Maximum target size for each text chunk.
-   **Chunk overlap:** Repeated text between adjacent chunks to preserve
    context.
-   **Embedding model:** Must be the same compatible model used when
    indexing and querying.
-   **Vector-store directory and collection:** Must point to the
    intended persistent index.
-   **Retrieval count (`k`):** Number of candidate chunks returned for
    grading.
-   **Grading threshold or prompt:** Determines how retrieved context is
    evaluated.
-   **Generation model:** Local LLM used to formulate the final
    response.

The development setup has used a chunk size of 800 characters/tokens as
configured in code and an overlap of 100; confirm the chunker's unit
before interpreting those values. Actual configuration variable names
should be documented here when finalized.

## Design Decisions

### Why Corrective RAG instead of basic RAG?

Basic RAG usually retrieves passages and immediately generates an
answer. Corrective RAG adds a quality check so weak retrieval can
trigger a correction path rather than being accepted without evaluation.

### Why Ollama?

Ollama makes it possible to run supported language and embedding models
locally, reducing reliance on hosted model APIs. Local execution still
requires sufficient hardware resources.

### Why ChromaDB?

Chroma provides a practical vector store for indexing, similarity
search, and persistence during local development.

### Why separate the modules?

Separating ingestion, retrieval, grading, correction, and generation
makes the pipeline easier to test, debug, and extend.

## Current Scope and Roadmap

The repository is being developed incrementally. The core development
work has included PDF loading, chunking, embeddings, Chroma storage,
semantic retrieval, and retrieval-grader testing.

Potential next steps include:

-   [ ] Complete and validate the end-to-end corrective retrieval loop.
-   [ ] Add query rewriting and a bounded retry policy.
-   [ ] Add an explicit "insufficient evidence" response.
-   [ ] Expose the pipeline through a FastAPI service.
-   [ ] Build a UI for document management, questions, retrieved
    evidence, and answers.
-   [ ] Add request validation, structured logging, and error handling.
-   [ ] Add evaluation datasets and retrieval-quality metrics.
-   [ ] Add optional external search as a clearly controlled fallback.
-   [ ] Add document-level isolation and metadata filters for
    multi-document use.

Mark a roadmap item as complete only after it is implemented and tested
in the repository.

## Troubleshooting

### `ModuleNotFoundError: No module named 'app'`

Run commands from the repository root and use module-based test
execution:

``` bash
python -m pytest -v
```

Check that the intended package files and `__init__.py` files are
present where required by the current project structure.

### Ollama model not found

Check installed models and pull the required model:

``` bash
ollama list
ollama pull nomic-embed-text
ollama pull qwen3:8b
```

### Ollama connection error

Make sure the Ollama service is running and that the application is
configured to use the correct local Ollama endpoint.

### Retrieval returns irrelevant chunks

-   Verify that the source document was parsed correctly.
-   Inspect the chunk text and metadata.
-   Confirm the query and document embeddings use the same model.
-   Test different retrieval counts and chunk sizes.
-   Inspect the grader's input and output before changing the prompt.
-   Rebuild the index if the embedding model changes.

### Chroma returns dimension mismatch errors

An index created with one embedding model may not be compatible with
another model that produces vectors of a different dimension. Use a
separate collection or rebuild the index with the selected embedding
model.

### Tests cannot import project modules

Confirm the active virtual environment, current working directory,
package structure, and dependency installation. Prefer
`python -m pytest` from the project root.

## Security Notes

-   Never commit `.env` files, API keys, access tokens, passwords, or
    private certificates.
-   Do not commit virtual environments, caches, generated model files,
    or large local vector databases.
-   Do not publish confidential HR, finance, employee, or company
    documents.
-   Treat retrieved documents as untrusted input. A document can contain
    incorrect information or malicious instructions.
-   Keep generated answers grounded in retrieved evidence and make
    uncertainty explicit.
-   If external search is added, validate sources and avoid sending
    confidential user queries or document content to external services
    without authorization.

## Contributing

Contributions and improvements are welcome.

1.  Create a feature branch.
2.  Make a focused change.
3.  Add or update tests.
4.  Run `python -m pytest -v`.
5.  Open a pull request describing the change and its validation.

## License

No license has been specified yet. Add a `LICENSE` file before
presenting the project as open source, and choose a license appropriate
for how you want others to use and distribute the code.
