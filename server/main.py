from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

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

# Additional hello endpoint with path parameter
@app.get("/hello/{name}")
async def hello_name(name: str):
    """
    Personalized hello endpoint
    """
    return {"message": f"Hello, {name}!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 