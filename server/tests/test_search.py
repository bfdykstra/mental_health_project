#!/usr/bin/env python3
"""
Test script for the search functionality.
"""

import sys
import os
import json

# Now import from scripts
from embeddings.search_embeddings import EmbeddingSearcher

def main():
    """Example usage of the embedding searcher."""
    try:
        # Initialize searcher
        searcher = EmbeddingSearcher()
        
        # Example 1: Semantic search
        print("\n🔍 Example 1: Semantic Search")
        query = "I feel anxious and overwhelmed with stress"
        results = searcher.search(query, top_k=3)
        
        print(f"\nQuery: '{query}'")
        print(f"Found {len(results)} results:")
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. Similarity: {result['similarity_score']:.3f}")
            print(f"   Prompt: {result['prompt'][:100]}...")
            print(f"   Keywords: {result['metadata']['search_keywords']}")
            quality_buckets = result['metadata']['quality_buckets']
            if quality_buckets:
                print(f"   Quality levels: {quality_buckets}")
        
        # Example 2: Keyword-based search
        print("\n🔍 Example 2: Keyword-based Search")
        keywords = ["Weight Management", "Substance Use & Addiction"]
        keyword_results = searcher.search_by_keywords(keywords, top_k=3)
        
        print(f"\nSearching for keywords: {keywords}")
        print(f"Found {len(keyword_results)} results:")
        
        for i, result in enumerate(keyword_results, 1):
            print(f"\n{i}. Prompt: {result['prompt'][:100]}...")
            print(f"   Matching keywords: {result['matching_keywords']}")
            print(f"   All keywords: {result['metadata']['search_keywords']}")
        
        # Example 3: Combined search and keyword filter
        print("\n🔍 Example 3: Semantic Search with Keyword Filter")
        filtered_results = searcher.search(
            "I have trouble sleeping and feel tired",
            top_k=5,
            keyword_filter=["Sleep & Fatigue"]
        )
        
        print(f"\nFound {len(filtered_results)} results with Sleep & Fatigue keyword:")
        for i, result in enumerate(filtered_results, 1):
            print(f"\n{i}. Similarity: {result['similarity_score']:.3f}")
            print(f"   Prompt: {result['prompt'][:100]}...")
            print(f"   Keywords: {result['metadata']['search_keywords']}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        raise

if __name__ == "__main__":
    main()