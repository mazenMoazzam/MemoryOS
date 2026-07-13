# MemoryOS

## What is this project?

MemoryOS represents a memory layer for AI agents. Right now AI assistants forget everything between conversations. MemoryOS fixes that by storing what the user says, embedding it into vectors, and retrieving relevant past context whenever the user asks something new. The goal is to make AI agents feel like they actually remember you and your work across numerous sessions

## What is being built

- A C++ engine that stores and searches vector embeddings using HNSW indexing
- A FastAPI backend that handles conversations, calls OpenAI for embeddings, and queries the memory engine
- PostgreSQL for storing raw memory text and session metadata
- A React frontend for interacting with the system

## Tech Stack

- C++ with hnswlib for vector search
- pybind11 to call the C++ engine from Python
- Python / FastAPI for the backend API
- PostgreSQL for metadata storage
- OpenAI API for embeddings and LLM responses
- React for the frontend

---

## What has been done so far

### C++ Memory Engine

The core of the project is a custom vector search engine written in C++. It lives in the `memory_engine/` folder.

**What it does:**
- Takes a vector (a list of floats or decimals representing a memory) and stores it in an HNSW index
- Given a specific query vector, it searches the index and returns the top K most similar vectors by L2 distance
- Can save and load the index to and from disk so memories persist between runs
- Exposed to Python via pybind11 so the FastAPI backend can call it directly whenever it is needed

**How the C++ code works:**

`engine.h` defines the `MemoryEngine` class with four main methods:
- `addVector(id, embedding)` - stores a vector with a given integer ID
- `search(query, top_k)` - returns the top K closest vectors to the query
- `saveIndex(path)` - writes the index to disk
- `loadIndex(path)` - loads a previously saved index from disk

`engine.cpp` implements those methods using hnswlib. The index uses L2 (Euclidean) distance to measure how similar two vectors are. Lower score means more similar. When you search, it returns a sorted list of `SearchResult` structs, each containing an `id` and a `score`.

`bindings.cpp` uses pybind11 to wrap the C++ class so it can be imported in Python like a normal module:

```python
from memory_engine import MemoryEngine

engine = MemoryEngine(dim=1536, max_elements=10000)
engine.add_vector(1, [...])  # store a memory
results = engine.search([...], 5)  # find 5 closest memories
```

The engine is built using CMake and compiles to a `.so` file that Python imports directly.

---

## Project Structure

```
MemoryOS/
├── memory_engine/
│   ├── engine.h          - C++ class definition
│   ├── engine.cpp        - vector storage and search logic
│   ├── bindings.cpp      - pybind11 Python bindings
│   └── CMakeLists.txt    - build config
└── README.md
```

---

### FastAPI Backend

The backend is built with FastAPI and handles the full memory flow. This includes receiving messages, embedding them, searching the C++ engine, and returning responses.

It is split into three services:

**services/embedding.py**

Calls the OpenAI Embeddings API and converts raw text into a vector of 1536 floats. I chose text-embedding-3-small over text-embedding-ada-002 because it is cheaper, faster, and performs about the same for this use case.

**services/llm.py**

Calls GPT-4o with a system prompt that injects relevant past memories before the user message. I kept this in its own file so I can swap models later without touching anything else. The memory injection happens here where retrieved memories get formatted and prepended to the system prompt so the model has full context before it responds.

**db/postgres.py**

Handles all PostgreSQL interactions. There are two tables:

- memories — stores the raw text of each memory, the vector ID that links it to the C++ engine, the session it came from, and a timestamp
- sessions — stores session metadata per user

The reason vector_id exists is because the C++ engine and PostgreSQL need to stay in sync. The C++ engine only knows numbers not text. So when the C++ engine finds the top 5 closest vectors and returns their IDs, PostgreSQL uses those IDs to look up and return the actual text of those memories.

I chose to run PostgreSQL in a Docker container instead of installing it locally because it keeps the setup clean and reproducible. Anyone can clone this repo, run docker compose up -d, and have a fully working database in seconds without configuring anything manually. It also means when this eventually gets deployed, Docker is already part of the setup.

---

## Setup

### Build the C++ engine

```bash
brew install cmake pybind11
cd memory_engine
mkdir build && cd build
cmake ..
make
```

### Start the database

```bash
docker compose up -d
```

### Run the backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
