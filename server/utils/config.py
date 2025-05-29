#!/usr/bin/env python3
"""
Centralized configuration management.
"""

import os
from dataclasses import dataclass
from typing import List

@dataclass
class Config:
    # API Configuration
    openai_api_key: str = os.getenv('OPENAI_API_KEY', '')
    embedding_model: str = "text-embedding-ada-002"
    tagging_model: str = "gpt-4o-mini"
    
    # Database Configuration
    chroma_db_path: str = "./chroma_db"
    collection_name: str = "pair_prompt_embeddings"
    
    # Processing Configuration
    batch_size: int = 100
    max_concurrent: int = 10
    
    # File Paths
    data_file: str = "data/pair_data_tagged.csv"

config = Config() 