#!/usr/bin/env python3
"""
Therapy Response Synthesizer

This module provides functionality to synthesize high-quality therapy responses
by finding similar patient conversations and using their high-quality responses
as examples for an LLM to generate a contextually appropriate response.
"""

import sys
import os

from typing import List, Dict, Any, Optional, AsyncGenerator
import logging
import asyncio
from embeddings.search_embeddings import EmbeddingSearcher
from utils.llm_utils import llm_client

from utils.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def synthesize_therapy_response(
    user_query: str,
    keywords: Optional[List[str]] = None,
    top_k: int = 5
) -> Dict[str, Any]:
    """
    Synthesize a therapy response based on similar patient conversations.
    
    This function:
    1. Searches for similar patient conversations using semantic search
    2. Extracts high-quality therapist responses from the similar examples
    3. Uses an LLM to synthesize a response based on the examples
    4. Returns structured results including examples and synthesized response
    
    Args:
        user_query: Free text query containing patient transcript and/or question
        keywords: Optional list of keywords to filter search results
        top_k: Number of similar examples to retrieve (default: 5)
        
    Returns:
        Dictionary containing:
        - similar_examples: List of similar patient conversations with metadata
        - synthesized_response: LLM-generated response based on examples
        - keywords: Keywords used for search (or empty list if none)
        - user_query: Original user query
    """
    logger.info(f"Starting therapy response synthesis for query: {user_query[:100]}...")
    
    # Initialize keywords if None
    if keywords is None:
        keywords = []
    
    try:
        # Initialize the embedding searcher
        searcher = EmbeddingSearcher()
        
        # Search for similar examples
        logger.info(f"Searching for {top_k} similar examples with keywords: {keywords}")
        similar_examples = searcher.search(
            query=user_query,
            top_k=top_k,
            keyword_filter=keywords if keywords else None,
            include_metadata=True
        )
        
        if not similar_examples:
            logger.warning("No similar examples found")
            return {
                "similar_examples": [],
                "synthesized_response": "I apologize, but I couldn't find any similar examples to help generate a response. Please provide more context or try different keywords.",
                "keywords": keywords,
                "user_query": user_query
            }
        
        logger.info(f"Found {len(similar_examples)} similar examples")
        
        # Extract high-quality responses from similar examples
        high_quality_examples = []
        for example in similar_examples:
            metadata = example.get('metadata', {})
            
            # quality_buckets is guaranteed to be a dictionary from EmbeddingSearcher
            quality_buckets = metadata.get('quality_buckets', {})
            
            # Get high-quality responses if available
            hq_responses = quality_buckets.get('high_quality', [])
            if hq_responses:
                high_quality_examples.append({
                    'prompt': example['prompt'],
                    'high_quality_responses': hq_responses,
                    'similarity_score': example.get('similarity_score', 0)
                })
            else:
                logger.warning(f"No high quality responses found for example with row_index: {metadata.get('row_index', 'unknown')}")
                # Continue without raising error - skip examples without high quality responses
        
        # Check if we found any high-quality examples
        if not high_quality_examples:
            logger.warning("No high-quality examples found in similar results")
            return {
                "similar_examples": similar_examples,
                "synthesized_response": "I found similar examples but none had high-quality responses available. Please try different keywords or provide more context.",
                "keywords": keywords,
                "user_query": user_query
            }
        
        # Generate synthesized response using LLM
        synthesized_response = _generate_synthesized_response(
            user_query=user_query,
            high_quality_examples=high_quality_examples
        )
        
        return {
            "similar_examples": similar_examples,
            "synthesized_response": synthesized_response,
            "keywords": keywords,
            "user_query": user_query
        }
        
    except Exception as e:
        logger.error(f"Error in therapy response synthesis: {e}")
        return {
            "similar_examples": [],
            "synthesized_response": f"An error occurred while generating the response: {str(e)}",
            "keywords": keywords,
            "user_query": user_query
        }

def _generate_synthesized_response(
    user_query: str,
    high_quality_examples: List[Dict[str, Any]]
) -> str:
    """
    Generate a synthesized therapy response using LLM with high-quality examples as context.
    
    Args:
        user_query: The user's query containing patient information and question
        high_quality_examples: List of similar examples with their high-quality responses
        
    Returns:
        Synthesized therapy response
    """
    try:
        # Build the prompt with examples
        prompt = _build_synthesis_prompt(user_query, high_quality_examples)
        
        # Call the LLM
        response = llm_client.sync_client.chat.completions.create(
            model=Config.synthesis_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert mental health therapist. Your role is to provide thoughtful, empathetic, and clinically sound responses to patients based on similar examples of high-quality therapeutic interactions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        logger.error(f"Error generating synthesized response: {e}")
        return "I apologize, but I encountered an error while generating a response. Please try again or consult with a supervisor."

def _build_synthesis_prompt(
    user_query: str,
    high_quality_examples: List[Dict[str, Any]]
) -> str:
    """
    Build the prompt for the LLM to synthesize a therapy response using reflective listening principles.
    
    Args:
        user_query: The user's query
        high_quality_examples: Examples with high-quality responses (hq1, hq2)
        
    Returns:
        Formatted prompt string incorporating reflective listening skills
    """
    prompt = """You are an expert mental health therapist specializing in reflective listening techniques. Your role is to provide therapeutic responses that demonstrate core reflective listening skills based on similar high-quality patient interactions.

REFLECTIVE LISTENING FRAMEWORK:
1. EMPATHY: Understand the patient's internal frame of reference rather than imposing external judgments
2. ACCEPTANCE: Show unconditional respect for the person without agreement/disagreement  
3. VALIDATION: Acknowledge and affirm the patient's emotions and experiences as legitimate
4. REFLECTION: Mirror back what you hear in the patient's own words, focusing on feelings and meaning
5. CONCRETENESS: Help the patient explore specific situations rather than vague generalities

Below are examples of similar patient situations and high-quality therapeutic responses that demonstrate reflective listening:

"""
    
    # Add examples with reflective listening analysis
    for i, example in enumerate(high_quality_examples, 1):
        prompt += f"--- Example {i} ---\n"
        prompt += f"Patient Statement: {example['prompt']}\n"
        prompt += f"High-Quality Reflective Responses:\n"
        
        for j, response in enumerate(example['high_quality_responses'], 1):
            prompt += f"{j}. {response}\n"
        
        prompt += "\n"
      
    prompt += f"""--- Current Patient Statement ---
{user_query}

INSTRUCTIONS FOR YOUR RESPONSE:
Using reflective listening principles, provide a therapeutic response that:

1. REFLECTS THE PATIENT'S PERSPECTIVE: Use their own words and frame of reference, not your interpretation
2. VALIDATES EMOTIONS: Acknowledge the feelings present in their statement as real and understandable  
3. DEMONSTRATES EMPATHY: Show you understand their internal experience without judgment
4. FOCUSES ON THE PERSON: Respond to what is personal rather than abstract or impersonal details
5. ENCOURAGES EXPLORATION: Create space for the patient to go deeper into their thoughts and feelings

REFLECTIVE LISTENING TECHNIQUES TO USE:
- Simple reflection: "You feel that..." or "It sounds like..."
- Feeling reflection: Identify and reflect the emotions you hear
- Meaning reflection: Reflect the underlying significance or values expressed
- Double-sided reflection: Acknowledge ambivalence when present ("On one hand... and on the other hand...")

Provide a brief explanation of how that response demonstrates reflective listening.

AVOID:
- Giving advice or solutions unless specifically requested
- Asking multiple questions 
- Imposing your own frame of reference
- Minimizing or dismissing their concerns
- Being overly clinical or detached

Your reflective listening response and explanation of how that response demonstrates reflective listening:"""
    
    return prompt 

async def synthesize_therapy_response_streaming(
    user_query: str,
    keywords: Optional[List[str]] = None,
    top_k: int = 5
) -> AsyncGenerator[Dict[str, Any], None]:
    """
    Async streaming version of therapy response synthesis.
    
    Yields real-time events during the synthesis process:
    - progress updates
    - similar examples as found
    - synthesized response chunks
    
    Args:
        user_query: Free text query containing patient transcript and/or question
        keywords: Optional list of keywords to filter search results
        top_k: Number of similar examples to retrieve (default: 5)
        
    Yields:
        Dictionary events with type, data, and timestamp
    """
    logger.info(f"Starting streaming therapy response synthesis for query: {user_query[:100]}...")
    
    # Initialize keywords if None
    if keywords is None:
        keywords = []
    
    try:
        # Yield initial progress
        yield {
            "type": "progress",
            "message": "Starting synthesis process...",
            "stage": "initialization",
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # Initialize the embedding searcher
        searcher = EmbeddingSearcher()
        
        # Yield search progress
        yield {
            "type": "progress",
            "message": f"Searching for {top_k} similar examples...",
            "stage": "search",
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # Search for similar examples (run in thread to avoid blocking)
        similar_examples = await asyncio.to_thread(
            searcher.search,
            query=user_query,
            top_k=top_k,
            keyword_filter=keywords if keywords else None,
            include_metadata=True
        )
        
        if not similar_examples:
            yield {
                "type": "error",
                "message": "No similar examples found",
                "timestamp": asyncio.get_event_loop().time()
            }
            return
        
        # Yield similar examples as they're processed
        yield {
            "type": "similar_examples",
            "data": similar_examples,
            "count": len(similar_examples),
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # Extract high-quality responses
        yield {
            "type": "progress",
            "message": "Processing high-quality examples...",
            "stage": "processing",
            "timestamp": asyncio.get_event_loop().time()
        }
        
        high_quality_examples = []
        for example in similar_examples:
            metadata = example.get('metadata', {})
            quality_buckets = metadata.get('quality_buckets', {})
            hq_responses = quality_buckets.get('high_quality', [])
            if hq_responses:
                high_quality_examples.append({
                    'prompt': example['prompt'],
                    'high_quality_responses': hq_responses,
                    'similarity_score': example.get('similarity_score', 0)
                })
        
        if not high_quality_examples:
            yield {
                "type": "error",
                "message": "No high-quality examples found",
                "timestamp": asyncio.get_event_loop().time()
            }
            return
        
        # Generate synthesized response with streaming
        yield {
            "type": "progress",
            "message": "Generating therapeutic response...",
            "stage": "synthesis",
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # Stream the LLM response
        synthesized_response = ""
        async for chunk in _generate_synthesized_response_streaming(
            user_query=user_query,
            high_quality_examples=high_quality_examples
        ):
            synthesized_response += chunk
            yield {
                "type": "response_chunk",
                "chunk": chunk,
                "accumulated_response": synthesized_response,
                "timestamp": asyncio.get_event_loop().time()
            }
        
        # Yield final complete result
        yield {
            "type": "complete",
            "data": {
                "similar_examples": similar_examples,
                "synthesized_response": synthesized_response,
                "keywords": keywords,
                "user_query": user_query
            },
            "timestamp": asyncio.get_event_loop().time()
        }
        
    except Exception as e:
        logger.error(f"Error in streaming therapy response synthesis: {e}")
        yield {
            "type": "error",
            "message": str(e),
            "timestamp": asyncio.get_event_loop().time()
        }

async def _generate_synthesized_response_streaming(
    user_query: str,
    high_quality_examples: List[Dict[str, Any]]
) -> AsyncGenerator[str, None]:
    """
    Generate a synthesized therapy response using streaming LLM with high-quality examples as context.
    
    Args:
        user_query: The user's query containing patient information and question
        high_quality_examples: List of similar examples with their high-quality responses
        
    Yields:
        String chunks of the synthesized response
    """
    try:
        # Build the prompt with examples
        prompt = _build_synthesis_prompt(user_query, high_quality_examples)
        
        # Stream the LLM response
        stream = await asyncio.to_thread(
            llm_client.sync_client.chat.completions.create,
            model=Config.synthesis_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert mental health therapist. Your role is to provide thoughtful, empathetic, and clinically sound responses to patients based on similar examples of high-quality therapeutic interactions."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1000,
            stream=True
        )
        
        # Yield chunks as they arrive
        for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
        
    except Exception as e:
        logger.error(f"Error generating streaming synthesized response: {e}")
        yield "I apologize, but I encountered an error while generating a response. Please try again or consult with a supervisor." 