from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging

from therapy_response_synthesizer import synthesize_therapy_response

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pydantic models for request/response
class TherapyRequest(BaseModel):
    user_query: str = Field(..., description="The user's query containing patient information and question")
    keywords: Optional[List[str]] = Field(None, description="Optional list of keywords to filter search results")
    top_k: int = Field(5, ge=1, le=20, description="Number of similar examples to retrieve (1-20)")

class SimilarExample(BaseModel):
    prompt: str
    similarity_score: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

class TherapyResponse(BaseModel):
    similar_examples: List[SimilarExample]
    synthesized_response: str
    keywords: List[str]
    user_query: str

# Create FastAPI instance
app = FastAPI(
    title="Mental Health API",
    description="A simple FastAPI application for mental health project",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Hello World route
@app.get("/")
async def hello_world():
    """
    Simple hello world endpoint
    """
    return {"message": "Hello, World!"}

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "healthy", "service": "Mental Health API"}


# Therapy Response Synthesis endpoint
@app.post("/synthesize-therapy-response", response_model=TherapyResponse)
async def synthesize_therapy_response_endpoint(request: TherapyRequest):
    """
    Synthesize a therapy response based on similar patient conversations.
    
    This endpoint:
    1. Searches for similar patient conversations using semantic search
    2. Extracts high-quality therapist responses from the similar examples
    3. Uses an LLM to synthesize a response based on the examples
    4. Returns structured results including examples and synthesized response
    
    Args:
        request: TherapyRequest containing user_query, optional keywords, and top_k
        
    Returns:
        TherapyResponse containing similar examples and synthesized response
        
    Raises:
        HTTPException: If synthesis fails or invalid parameters provided
    """
    try:
        logger.info(f"Received therapy synthesis request for query: {request.user_query[:100]}...")
        
        # Validate input
        if not request.user_query.strip():
            raise HTTPException(status_code=400, detail="user_query cannot be empty")
        
        # Call the synthesis function
        result = synthesize_therapy_response(
            user_query=request.user_query,
            keywords=request.keywords,
            top_k=request.top_k
        )
        
        # Convert result to response model
        similar_examples = [
            SimilarExample(
                prompt=example['prompt'],
                similarity_score=example.get('similarity_score'),
                metadata=example.get('metadata')
            )
            for example in result['similar_examples']
        ]
        
        response = TherapyResponse(
            similar_examples=similar_examples,
            synthesized_response=result['synthesized_response'],
            keywords=result['keywords'],
            user_query=result['user_query']
        )
        
        logger.info("Successfully synthesized therapy response")
        return response
        
    except ValueError as e:
        logger.error(f"Validation error in therapy synthesis: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in therapy synthesis: {e}")
        raise HTTPException(status_code=500, detail="Internal server error occurred during synthesis")

# Test endpoint for therapy synthesis with example data
@app.get("/test-synthesis")
async def test_therapy_synthesis():
    """
    Test endpoint that calls the therapy synthesis with example data.
    Useful for quick testing without needing to construct a POST request.
    """
    try:
        example_query = """
        Patient: "I've been feeling really overwhelmed lately with work and family responsibilities. 
        I can't seem to find time for myself and I'm starting to feel burned out. Sometimes I just 
        want to run away from everything. How do I deal with these feelings?"
        
        Question: How should a therapist respond to this patient who is expressing feelings of 
        overwhelm and burnout?
        """
        
        result = synthesize_therapy_response(
            user_query=example_query,
            keywords=None,
            top_k=3
        )
        
        return {
            "message": "Test synthesis completed successfully",
            "result": result
        }
        
    except Exception as e:
        logger.error(f"Error in test synthesis: {e}")
        raise HTTPException(status_code=500, detail=f"Test synthesis failed: {str(e)}")



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 