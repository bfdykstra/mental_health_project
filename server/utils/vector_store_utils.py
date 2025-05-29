#!/usr/bin/env python3
"""
Centralized vector store utilities for ChromaDB operations.
Provides consistent database connection, collection management, and search operations.
"""

import chromadb
from typing import List, Dict, Optional, Any
import json
import logging

class VectorStore:
    """Centralized ChromaDB operations"""
    
    def __init__(self, db_path: str = "./chroma_db", collection_name: str = "pair_prompt_embeddings"):
        self.db_path = db_path
        self.collection_name = collection_name
        self._client = None
        self._collection = None
    
    @property
    def client(self):
        """Lazy-loaded ChromaDB client"""
        if self._client is None:
            self._client = chromadb.PersistentClient(path=self.db_path)
        return self._client
    
    @property
    def collection(self):
        """Get or create collection"""
        if self._collection is None:
            try:
                self._collection = self.client.get_collection(self.collection_name)
            except:
                # Collection doesn't exist, create it
                self._collection = self.client.create_collection(
                    name=self.collection_name,
                    metadata={"description": "Embeddings for mental health prompts with quality buckets and search keywords"}
                )
        return self._collection
    
    def recreate_collection(self):
        """Delete and recreate collection for fresh start"""
        try:
            self.client.delete_collection(name=self.collection_name)
            logging.info(f"Deleted existing collection: {self.collection_name}")
        except:
            pass  # Collection didn't exist
        
        self._collection = self.client.create_collection(
            name=self.collection_name,
            metadata={"description": "Embeddings for mental health prompts with quality buckets and search keywords"}
        )
        return self._collection
    
    def add_embeddings_batch(self, embeddings: List[List[float]], documents: List[str], 
                           metadatas: List[Dict], ids: List[str], batch_size: int = 100):
        """Add embeddings in batches with progress tracking"""
        from tqdm import tqdm
        
        for i in tqdm(range(0, len(embeddings), batch_size), desc="Adding to ChromaDB"):
            end_idx = min(i + batch_size, len(embeddings))
            
            self.collection.add(
                embeddings=embeddings[i:end_idx],
                documents=documents[i:end_idx],
                metadatas=metadatas[i:end_idx],
                ids=ids[i:end_idx]
            )
    
    def search(self, query_embedding: List[float], top_k: int = 5, 
              where_clause: Optional[Dict] = None) -> Dict[str, Any]:
        """Unified search interface"""
        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=['documents', 'metadatas', 'distances'],
            where=where_clause
        )
    
    def get_documents(self, where_clause: Optional[Dict] = None, limit: int = None) -> Dict[str, Any]:
        """Get documents with optional filtering"""
        kwargs = {
            'include': ['documents', 'metadatas'],
            'where': where_clause
        }
        if limit:
            kwargs['limit'] = limit
        return self.collection.get(**kwargs)
    
    def build_keyword_filter(self, keywords: List[str]) -> Optional[Dict]:
        """Build ChromaDB where clause for keyword filtering"""
        if not keywords:
            return None
            
        if len(keywords) == 1:
            return {keywords[0]: True}
        else:
            return {"$or": [{keyword: True} for keyword in keywords]}
    
    def get_count(self) -> int:
        """Get total number of documents in collection"""
        return self.collection.count()

# Global instance for convenience
vector_store = VectorStore() 