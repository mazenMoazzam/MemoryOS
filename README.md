# MemoryOS

## What is this?

MemoryOS is a memory layer for AI agents. Right now AI assistants forget everything between conversations. MemoryOS fixes that by storing what the user says, embedding it into vectors, and retrieving relevant past context whenever the user asks something new. The goal is to make AI agents feel like they actually remember you and your work across sessions.

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
- Takes a vector (a list of floats representing a memory) and stores it in an HNSW index
- Given a query vector, searches the index and returns the top K most similar vectors by L2 distance
- Can save and load the index to and from disk so memories persist between runs
- Exposed to Python via pybind11 so the FastAPI backend can call it directly

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

## Setup

### Build the C++ engine

```bash
brew install cmake pybind11
cd memory_engine
mkdir build && cd build
cmake ..
make
```

This produces `memory_engine.cpython-39-darwin.so` in the build folder which Python imports directly.
