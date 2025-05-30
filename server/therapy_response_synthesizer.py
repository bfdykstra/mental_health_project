#!/usr/bin/env python3
"""
Therapy Response Synthesizer

This module provides functionality to synthesize high-quality therapy responses
by finding similar patient conversations and using their high-quality responses
as examples for an LLM to generate a contextually appropriate response.
"""

import sys
import os

from typing import List, Dict, Any, Optional
import logging
from embeddings.search_embeddings import EmbeddingSearcher
from utils.llm_utils import llm_client

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
    2. Extracts high-quality responses from the similar examples
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
            model="gpt-4.1",
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
    Build the prompt for the LLM to synthesize a therapy response.
    
    Args:
        user_query: The user's query
        high_quality_examples: Examples with high-quality responses
        
    Returns:
        Formatted prompt string
    """
    prompt = """You are tasked with providing a high-quality therapeutic response based on similar patient interactions.

Below are examples of similar patient situations and the high-quality responses that therapists provided:

"""
    
    # Add examples
    for i, example in enumerate(high_quality_examples, 1):
        prompt += f"--- Example {i} ---\n"
        prompt += f"Patient Situation: {example['prompt']}\n"
        prompt += f"High-Quality Therapist Responses:\n"
        
        for j, response in enumerate(example['high_quality_responses'], 1):
            prompt += f"{j}. {response}\n"
      
    prompt += f"""--- Current Situation ---
{user_query}

Based on the high-quality examples above, please provide a thoughtful, empathetic, and clinically appropriate response. Consider:
1. The therapeutic techniques demonstrated in the examples
2. The tone and approach used in high-quality responses  
3. The specific context and needs presented in the current situation
4. Professional boundaries and best practices

Your synthesized response:"""
    
    return prompt 