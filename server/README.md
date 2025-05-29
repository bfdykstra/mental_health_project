# Mental Health Prompt Embeddings

This project creates embeddings from mental health prompts and stores them in ChromaDB for semantic search, and provides a FastAPI web service for accessing the data.

## Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Set up OpenAI API key:**
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## FastAPI Web Service

### Running the API

To start the FastAPI server:

```bash
# Option 1: Using the run script
python run_server.py

# Option 2: Using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Option 3: Running the main file directly
python main.py
```

The API will be available at `http://localhost:8000`

### API Endpoints

- **GET /** - Hello world endpoint

  ```
  Response: {"message": "Hello, World!"}
  ```

- **GET /health** - Health check endpoint

  ```
  Response: {"status": "healthy", "service": "Mental Health API"}
  ```

- **GET /hello/{name}** - Personalized hello endpoint
  ```
  Example: GET /hello/John
  Response: {"message": "Hello, John!"}
  ```

### API Documentation

Once the server is running, you can access:

- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc
- **OpenAPI schema**: http://localhost:8000/openapi.json

## Usage

### 1. Create Embeddings

Run the embedding creation script to process your CSV file and create the vector store:

```bash
python create_embeddings.py
```

This script will:

- Read the `data/pair_data_tagged.csv` file
- Generate embeddings for each prompt using OpenAI's `text-embedding-ada-002` model
- Store embeddings in ChromaDB with metadata including:
  - Original prompt text
  - Search keywords
  - Quality buckets (high, medium, low quality responses)
- Save the vector store to `./chroma_db/`

### 2. Search Embeddings

Use the search script to find similar prompts:

```bash
python search_embeddings.py
```

This script demonstrates various search capabilities:

- **Semantic search**: Find prompts similar to a query text
- **Quality filtering**: Filter results by response quality levels
- **Keyword filtering**: Filter by specific search keywords
- **Combined filtering**: Use both semantic similarity and keyword matching

## Data Structure

The CSV file should have the following columns:

| Column            | Description                                 |
| ----------------- | ------------------------------------------- |
| `prompt`          | The user's input or concern                 |
| `hq1`, `hq2`      | High quality responses                      |
| `mq1`             | Medium quality responses                    |
| `lq1` - `lq5`     | Low quality responses                       |
| `search_keywords` | Comma-separated keywords for categorization |

## Example Usage

```python
from search_embeddings import EmbeddingSearcher

# Initialize searcher
searcher = EmbeddingSearcher()

# Basic semantic search
results = searcher.search("I feel anxious and stressed", top_k=5)

# Search with quality filter (high quality only)
hq_results = searcher.search(
    "I can't sleep",
    top_k=3,
    quality_filter=['high_quality']
)

# Search with keyword filter
filtered_results = searcher.search(
    "weight loss motivation",
    top_k=5,
    keyword_filter=['Weight Management', 'Nutrition']
)

# Keyword-only search
keyword_results = searcher.search_by_keywords(['Anxiety', 'Depression'])
```

## Features

- **Semantic Search**: Find conceptually similar prompts even if they use different words
- **Quality Filtering**: Filter responses by quality levels (high/medium/low)
- **Keyword Filtering**: Filter by categorical search keywords
- **Persistent Storage**: Vector store is saved to disk and can be reused
- **Metadata Preservation**: All original data is preserved as searchable metadata
- **Batch Processing**: Efficient handling of large datasets
- **Error Handling**: Robust error handling for API calls and data processing

## Files

- `create_embeddings.py`: Main script to create embeddings from CSV
- `search_embeddings.py`: Script for searching and filtering embeddings
- `requirements.txt`: Python dependencies
- `data/pair_data_tagged.csv`: Input data file
- `chroma_db/`: Generated vector store directory (created after running the script)

## Notes

- The script uses OpenAI's `text-embedding-ada-002` model for generating embeddings
- ChromaDB provides persistent local storage for the vector database
- Embedding generation may take some time depending on the size of your dataset
- Make sure you have sufficient OpenAI API credits for the embedding generation
