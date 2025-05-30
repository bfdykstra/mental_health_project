#!/usr/bin/env python3
"""
Common data processing utilities for CSV handling and metadata parsing.
"""

import pandas as pd
import json
from typing import Dict, List, Any

def parse_quality_buckets(row: pd.Series) -> Dict[str, List[str]]:
    """Parse quality bucket columns and return non-empty values."""
    quality_buckets = {}
    
    # High quality buckets
    hq_buckets = [str(row[col]).strip() for col in ['hq1', 'hq2'] 
                  if col in row and pd.notna(row[col]) and str(row[col]).strip()]
    if hq_buckets:
        quality_buckets['high_quality'] = hq_buckets
    
    # Medium quality buckets
    mq_buckets = [str(row[col]).strip() for col in ['mq1'] 
                  if col in row and pd.notna(row[col]) and str(row[col]).strip()]
    if mq_buckets:
        quality_buckets['medium_quality'] = mq_buckets
    
    # Low quality buckets
    lq_buckets = [str(row[col]).strip() for col in ['lq1', 'lq2', 'lq3', 'lq4', 'lq5'] 
                  if col in row and pd.notna(row[col]) and str(row[col]).strip()]
    if lq_buckets:
        quality_buckets['low_quality'] = lq_buckets
    
    return quality_buckets

def parse_search_keywords(row: pd.Series) -> List[str]:
    """Parse search keywords from CSV row."""
    if 'search_keywords' not in row or pd.isna(row['search_keywords']):
        return []
    
    keywords_str = str(row['search_keywords']).strip()
    if not keywords_str:
        return []
    
    return [kw.strip() for kw in keywords_str.split(',') if kw.strip()]

def prepare_chroma_metadata(prompt: str, quality_buckets: Dict, search_keywords: List[str], row_index: int) -> Dict[str, Any]:
    """Prepare metadata for ChromaDB storage."""
    metadata = {
        "prompt": prompt,
        "quality_buckets": json.dumps(quality_buckets),
        "row_index": row_index
    }
    
    # Add each search keyword as a boolean field
    for keyword in search_keywords:
        if keyword:
            metadata[keyword] = True
    
    return metadata

def extract_keywords_from_metadata(metadata: Dict[str, Any]) -> List[str]:
    """Extract search keywords from ChromaDB metadata."""
    return [key for key, value in metadata.items() 
            if key not in ['prompt', 'quality_buckets', 'row_index'] and value is True]


def process_search_result_metadata(metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Process metadata from search results to extract keywords and quality buckets.
    
    This function ensures consistent metadata format:
    - quality_buckets: Always a dictionary (not JSON string)
    - search_keywords: Always a list of strings
    """
    processed_metadata = metadata.copy()
    
    # Extract search keywords from boolean fields
    search_keywords = extract_keywords_from_metadata(metadata)
    processed_metadata['search_keywords'] = search_keywords
    
    # Ensure quality_buckets is always a parsed dictionary
    quality_buckets = metadata.get('quality_buckets', '{}')
    
    # Check if it's already a dictionary
    if isinstance(quality_buckets, dict):
        print('found a dict')
        processed_metadata['quality_buckets'] = quality_buckets
    else:
        # If it's a string, parse it as JSON
        try:
            processed_metadata['quality_buckets'] = json.loads(quality_buckets)
        except Exception as e:
            print(f'Error parsing quality_buckets in process_search_result_metadata: {e}')
            print(f'quality_buckets type: {type(quality_buckets)}')
            print(f'quality_buckets value: {quality_buckets}')
            # Fallback to empty structure
            processed_metadata['quality_buckets'] = {
                'high_quality': [],
                'medium_quality': [],
                'low_quality': []
            }
    
    return processed_metadata 