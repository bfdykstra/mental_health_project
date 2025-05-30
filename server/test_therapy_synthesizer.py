#!/usr/bin/env python3
"""
Test script for the therapy response synthesizer.

This script demonstrates how to use the synthesize_therapy_response function
with various types of queries and keyword filters.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from therapy_response_synthesizer import synthesize_therapy_response
import json

def print_results(results: dict, title: str):
    """Pretty print the results of therapy response synthesis."""
    print(f"\n{'='*50}")
    print(f"{title}")
    print(f"{'='*50}")
    
    print(f"\nUser Query: {results['user_query']}")
    print(f"Keywords Used: {results['keywords']}")
    print(f"\nNumber of Similar Examples Found: {len(results['similar_examples'])}")
    
    # Print details of similar examples
    for i, example in enumerate(results['similar_examples'][:3], 1):  # Show top 3
        print(f"\n--- Similar Example {i} ---")
        print(f"Similarity Score: {example.get('similarity_score', 'N/A'):.3f}")
        print(f"Prompt Preview: {example['prompt'][:200]}...")
        
        # Show quality buckets if available
        metadata = example.get('metadata', {})
        quality_buckets = metadata.get('quality_buckets', {})
        if quality_buckets:
            print(f"Quality Buckets Available: {list(quality_buckets.keys())}")
            if 'high_quality' in quality_buckets:
                print(f"High Quality Responses: {len(quality_buckets['high_quality'])}")
    
    print(f"\n--- Synthesized Response ---")
    print(results['synthesized_response'])
    print(f"\n{'='*50}")

def main():
    """Run test cases for the therapy response synthesizer."""
    
    # Test Case 1: General therapy query without keywords
    test_query_1 = """
    Patient: "I've been feeling really overwhelmed lately with work and family responsibilities. 
    I can't seem to find time for myself and I'm starting to feel burned out. Sometimes I just 
    want to run away from everything. How do I deal with these feelings?"
    
    Question: How should a therapist respond to this patient who is expressing feelings of 
    overwhelm and burnout?
    """
    
    print("Testing Therapy Response Synthesizer...")
    results_1 = synthesize_therapy_response(
        user_query=test_query_1,
        keywords=None,
        top_k=5
    )
    print_results(results_1, "Test Case 1: General Overwhelm Query")
    
    # Test Case 2: Query with specific keywords
    test_query_2 = """
    Patient: "I keep having panic attacks when I have to speak in public. My heart races, 
    I start sweating, and I feel like I can't breathe. I have a big presentation coming up 
    at work and I'm terrified."
    
    Question: What therapeutic techniques would be most effective for this patient's public 
    speaking anxiety?
    """
    
    results_2 = synthesize_therapy_response(
        user_query=test_query_2,
        keywords=["Anxiety", "Coping Strategies"],
        top_k=5
    )
    print_results(results_2, "Test Case 2: Anxiety Query with Keywords")
    
    # Test Case 3: Brief query to test edge cases
    test_query_3 = "Patient says they feel sad. What should I do?"
    
    results_3 = synthesize_therapy_response(
        user_query=test_query_3,
        keywords=["Depression"],
        top_k=3
    )
    print_results(results_3, "Test Case 3: Brief Query")

if __name__ == "__main__":
    main() 