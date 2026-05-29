# Federal Open Market Committee (FOMC) Minutes Analysis — LLM RAG Project

## Overview

This project is a Retrieval-Augmented Generation (RAG) application designed to analyze Federal Open Market Committee (FOMC) meeting minutes using Large Language Models (LLMs).

The system allows users to:

* Query historical FOMC minutes using natural language
* Retrieve the most relevant sections from official documents
* Generate context-aware financial and economic insights
* Analyze monetary policy trends over time
* Explore inflation, interest rates, labor market discussions, and macroeconomic signals

The application combines:

* Document ingestion and preprocessing
* Vector embeddings and semantic search
* A vector database for retrieval
* An LLM for answer generation

---

# Features

* Retrieval-Augmented Generation (RAG) pipeline
* Semantic search on FOMC minutes
* Context-aware financial Q&A
* Historical monetary policy analysis
* PDF/Text document ingestion
* Embedding generation and vector storage
* Source-aware responses
* Scalable for additional economic reports and datasets

---

# Project Architecture

```text
                +-------------------+
                |   FOMC Minutes    |
                |  PDF/Text Files   |
                +---------+---------+
                          |
                          v
                +-------------------+
                | Document Loader   |
                +-------------------+
                          |
                          v
                +-------------------+
                | Text Chunking     |
                +-------------------+
                          |
                          v
                +-------------------+
                | Embedding Model   |
                +-------------------+
                          |
                          v
                +-------------------+
                | Vector Database   |
                +-------------------+
                          |
             User Query   |
                   +------v------+
                   | Retriever   |
                   +------+------+
                          |
                          v
                +-------------------+
                |       LLM         |
                +-------------------+
                          |
                          v
                +-------------------+
                | Generated Answer  |
                +-------------------+
```

---

# Tech Stack

## Programming Language

* Python

## LLM Frameworks

* LangChain / LlamaIndex (depending on implementation)

## Embedding Models

Examples:

* OpenAI Embeddings
* Sentence Transformers
* BGE Embeddings
* Instructor Embeddings

## Vector Database

Examples:

* PostgreSQL (pgvector)

## LLM Providers

* OpenAI GPT models



# Folder Structure

```text
project/
│
├── data/                  # FOMC minutes documents
├── TextPreprocessing/
|   ├── NltPreProc.py #To download the packages for the tokenization process. Running once
├── ├── TxtVector.py # Embed the vector with hugging faces all-MiniLM-L12-v2 network model.
├── DatabaseManagement/
│   ├── StoreVector.py       # Store in the embeddings and text chunks in the postgresql vectors database
├── .env
├── script.py  # To automate the whole process of vectors storage. NltPreProc.py script should be ran first.
├── TestQuery.py # To test the model. 
└── README.md
```

---

# Installation

## 0. PostgreSQL should be installed and the PGvector extension must also be installed. 

## 1. Clone the Repository

```bash
git clone https://github.com/Derozen/LLM_RAG_Fin.git
cd LLM_RAG_Fin
```


## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables


```env
OPENAI_API_KEY=your_api_key
```

---

# Data Collection

FOMC meeting minutes can be downloaded from the official Federal Reserve website.

Typical workflow:

1. Download FOMC minutes PDFs
2. Store them inside the `data/` directory
3. Run the ingestion pipeline
4. Generate embeddings
5. Store vectors inside the vector database

---

# Running the Project

## Store the text inside the vector database.

```bash
python TextPreprocessing/NltPreProc.py
python script.py
```

---

## Prompt you query

```bash
python TestQuery.py
```

---

# Example Queries

* "What was the Federal Reserve's stance on inflation in 2023?"
* "How did the FOMC discuss labor market conditions?"
* "What concerns were raised about interest rates?"
* "Compare monetary policy sentiment between 2020 and 2024."
* "Summarize the latest FOMC meeting minutes."

---


# Future Roadmap

* Deploy on cloud infrastructure
* Add authentication
* Build advanced analytics dashboard
* Add speech-to-text financial analysis
* Integrate market data APIs
* Add document summarization mode
* Improve retrieval accuracy with rerankers

---
