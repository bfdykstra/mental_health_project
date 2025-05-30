# Therapy Response Synthesis API

This API provides endpoints for synthesizing high-quality therapy responses based on similar patient conversations using semantic search and LLM generation.

## Quick Start

1. **Start the server:**

   ```bash
   python run_server.py
   ```

2. **Access API documentation:**

   - Interactive docs: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

3. **Test the API:**
   ```bash
   python test_api.py
   ```

## Endpoints

### 1. Main Synthesis Endpoint

**POST** `/synthesize-therapy-response`

Synthesizes a therapy response based on similar patient conversations.

#### Request Body:

```json
{
  "user_query": "Patient: 'I've been feeling anxious lately...' Question: How should I respond?",
  "keywords": ["Anxiety", "Coping Strategies"], // Optional
  "top_k": 5 // Optional, default: 5, range: 1-20
}
```

#### Response:

```json
{
  "similar_examples": [
    {
      "prompt": "Patient conversation text...",
      "similarity_score": 0.85,
      "metadata": {
        "quality_buckets": {...},
        "row_index": 123
      }
    }
  ],
  "synthesized_response": "Based on similar cases, I would suggest...",
  "keywords": ["Anxiety", "Coping Strategies"],
  "user_query": "Original query..."
}
```

### 2. Test Endpoints

**GET** `/test-synthesis`

- Quick test with example data
- No parameters required

**GET** `/synthesis-example`

- Returns example request format
- Helpful for understanding the API structure

### 3. Utility Endpoints

**GET** `/health`

- Health check endpoint

**GET** `/`

- Basic hello world endpoint

## Usage Examples

### Example 1: Basic Request (Python)

```python
import requests

response = requests.post(
    "http://localhost:8000/synthesize-therapy-response",
    json={
        "user_query": """
        Patient: "I keep having panic attacks when I have to speak in public.
        My heart races, I start sweating, and I feel like I can't breathe."

        Question: What therapeutic techniques would be most effective?
        """,
        "keywords": ["Anxiety", "Panic Attacks"],
        "top_k": 5
    }
)

result = response.json()
print(result["synthesized_response"])
```

### Example 2: Basic Request (curl)

```bash
curl -X POST "http://localhost:8000/synthesize-therapy-response" \
     -H "Content-Type: application/json" \
     -d '{
       "user_query": "Patient says they feel overwhelmed. What should I do?",
       "keywords": ["Stress"],
       "top_k": 3
     }'
```

### Example 3: JavaScript/Fetch

```javascript
const response = await fetch(
  "http://localhost:8000/synthesize-therapy-response",
  {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      user_query: "Patient: 'I can't sleep at night...' Question: How to help?",
      keywords: ["Sleep", "Insomnia"],
      top_k: 4,
    }),
  }
);

const result = await response.json();
console.log(result.synthesized_response);
```

## Parameters

### user_query (required)

- **Type:** string
- **Description:** The user's query containing patient information and question
- **Format:** Can include patient transcript, context, and specific questions
- **Example:** "Patient: 'I feel anxious about work.' Question: What coping strategies should I suggest?"

### keywords (optional)

- **Type:** array of strings
- **Description:** Keywords to filter search results for more relevant examples
- **Default:** null (no filtering)
- **Example:** ["Anxiety", "Work Stress", "Coping Strategies"]

### top_k (optional)

- **Type:** integer
- **Description:** Number of similar examples to retrieve
- **Default:** 5
- **Range:** 1-20
- **Example:** 3

## Response Fields

### similar_examples

Array of similar patient conversations found through semantic search:

- `prompt`: The original patient conversation text
- `similarity_score`: Semantic similarity score (0-1)
- `metadata`: Additional information including quality ratings

### synthesized_response

The LLM-generated therapy response based on high-quality examples from similar cases.

### keywords

The keywords that were used for filtering (either provided or empty list).

### user_query

Echo of the original user query for reference.

## Error Handling

The API returns standard HTTP status codes:

- **200**: Success
- **400**: Bad Request (invalid parameters)
- **500**: Internal Server Error

Error responses include a `detail` field with the error message:

```json
{
  "detail": "user_query cannot be empty"
}
```

## Best Practices

1. **Provide Context:** Include both patient information and your specific question
2. **Use Keywords:** Add relevant keywords to get more targeted examples
3. **Appropriate top_k:** Use 3-7 examples for most cases
4. **Handle Errors:** Always check response status and handle errors gracefully

## Troubleshooting

1. **Server not starting:**

   - Check if all dependencies are installed: `pip install -r requirements.txt`
   - Ensure the OpenAI API key is set in environment variables

2. **No similar examples found:**

   - Try broader keywords or remove keyword filters
   - Check if the embeddings database is properly set up

3. **Poor quality responses:**
   - Increase `top_k` to get more examples
   - Refine keywords to get more relevant examples
   - Ensure your query provides sufficient context
