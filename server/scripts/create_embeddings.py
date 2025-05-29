#!/usr/bin/env python3
"""
Refactored script using centralized utilities.
"""

import pandas as pd
from tqdm import tqdm

from llm_utils import llm_client
from vector_store_utils import vector_store  
from data_utils import parse_quality_buckets, parse_search_keywords, prepare_chroma_metadata

def process_csv_and_create_embeddings(csv_path="data/pair_data_tagged.csv"):
    """Main function using centralized utilities."""
    
    print("Reading CSV file...")
    df = pd.read_csv(csv_path)
    print(f"Loaded {len(df)} rows from CSV")
    
    print("Creating ChromaDB vector store...")
    collection = vector_store.recreate_collection()
    
    # Process data using utilities
    embeddings, documents, metadatas, ids = [], [], [], []
    
    print("Processing prompts and generating embeddings...")
    for idx, row in tqdm(df.iterrows(), total=len(df), desc="Creating embeddings"):
        prompt = str(row['prompt']).strip()
        if not prompt or prompt == 'nan':
            continue
        
        # Use centralized embedding function
        embedding = llm_client.get_embedding(prompt)
        if embedding is None:
            continue
        
        # Use utility functions for data processing
        quality_buckets = parse_quality_buckets(row)
        search_keywords = parse_search_keywords(row)
        metadata = prepare_chroma_metadata(prompt, quality_buckets, search_keywords, idx)
        
        embeddings.append(embedding)
        documents.append(prompt)
        metadatas.append(metadata)
        ids.append(f"prompt_{idx}")
    
    if embeddings:
        print(f"Adding {len(embeddings)} embeddings to ChromaDB...")
        vector_store.add_embeddings_batch(embeddings, documents, metadatas, ids)
        print(f"✅ Successfully created and stored {len(embeddings)} embeddings")
    
    return vector_store.client, collection

if __name__ == "__main__":
    process_csv_and_create_embeddings()