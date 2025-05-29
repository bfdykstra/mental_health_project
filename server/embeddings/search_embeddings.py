#!/usr/bin/env python3
"""
Script to search the embeddings vector store for similar prompts.

This script demonstrates how to:
1. Load the existing ChromaDB vector store
2. Perform semantic search on prompts
3. Filter results by quality buckets and search keywords
4. Return relevant prompts with metadata
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List, Dict, Optional, Any
import json

from utils.llm_utils import llm_client
from utils.vector_store_utils import vector_store
from utils.data_utils import extract_keywords_from_metadata, process_search_result_metadata

class EmbeddingSearcher:
    def __init__(self, chroma_db_path="./chroma_db", collection_name="pair_prompt_embeddings"):
        """Initialize the embedding searcher using centralized utilities."""
        # Configure the vector store with custom paths if provided
        if chroma_db_path != vector_store.db_path or collection_name != vector_store.collection_name:
            vector_store.db_path = chroma_db_path
            vector_store.collection_name = collection_name
            vector_store._client = None  # Reset client to use new path
            vector_store._collection = None  # Reset collection to use new name
        
        # Initialize connection (lazy-loaded)
        self.collection = vector_store.collection
        
        print(f"✅ Loaded collection '{collection_name}' with {vector_store.get_count()} documents")
    
    def search(
        self, 
        query: str, 
        top_k: int = 5,
        keyword_filter: Optional[List[str]] = None,
        include_metadata: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Search for similar prompts using semantic search.
        
        Args:
            query: The search query text
            top_k: Number of results to return
            keyword_filter: Filter by search keywords
            include_metadata: Whether to include metadata in results
            
        Returns:
            List of search results with prompts, distances, and metadata
        """
        # Get query embedding using centralized LLM client
        query_embedding = llm_client.get_embedding(query)
        if query_embedding is None:
            return []
        
        # Build where clause using utility function
        where_clause = vector_store.build_keyword_filter(keyword_filter)
        
        # Perform search using centralized vector store
        results = vector_store.search(query_embedding, top_k, where_clause)
        
        # Process results
        filtered_results = []
        
        for doc, metadata, distance in zip(
            results['documents'][0],
            results['metadatas'][0], 
            results['distances'][0]
        ):
            result = {
                'prompt': doc,
                'distance': distance,
                'similarity_score': 1 - distance  # Convert distance to similarity
            }
            
            if include_metadata:
                # Use utility function to process metadata
                result['metadata'] = process_search_result_metadata(metadata)
            
            filtered_results.append(result)
        
        return filtered_results
    
    def search_by_keywords(
        self, 
        keywords: List[str], 
        top_k: int = 5,
    ) -> List[Dict[str, Any]]:
        """
        Search for prompts that match specific keywords.
        
        Args:
            keywords: List of keywords to search for
            top_k: Number of results to return
            
        Returns:
            List of matching prompts
        """
        # Build where clause using utility function
        where_clause = vector_store.build_keyword_filter(keywords)
        
        # Get filtered documents using centralized vector store
        results = vector_store.get_documents(where_clause, top_k)
        
        matching_results = []
        
        for doc, metadata in zip(results['documents'], results['metadatas']):
            # Use utility function to extract keywords
            doc_keywords = extract_keywords_from_metadata(metadata)
            
            # Find which keywords matched (for display purposes)
            matching_keywords = [kw for kw in keywords if kw in doc_keywords]
            
            # Process metadata using utility function
            processed_metadata = process_search_result_metadata(metadata)
            
            matching_results.append({
                'prompt': doc,
                'metadata': processed_metadata,
                'matching_keywords': matching_keywords
            })
        
        return matching_results
    

