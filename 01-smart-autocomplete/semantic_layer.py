"""
SEMANTIC LAYER with caching for fast reloads
"""

import os
import pickle
import numpy as np
from sentence_transformers import SentenceTransformer

CACHE_DIR = "model_cache"

class SemanticSearch:
    def __init__(self):
        os.makedirs(CACHE_DIR, exist_ok=True)
        
        print("Loading semantic model...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        print("Model loaded!")
        
        self.word_vectors = {}
        self.words = []
    
    def index_words(self, word_list):
        cache_file = os.path.join(CACHE_DIR, "vectors_cache.pkl")
        
        # Check if we already indexed these exact words
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                cached = pickle.load(f)
                if cached.get('words') == word_list:
                    print("Using cached vectors!")
                    self.word_vectors = cached['vectors']
                    self.words = cached['words']
                    return
        
        # Fresh index
        print(f"Indexing {len(word_list)} words...")
        self.words = list(set(word_list))
        vectors = self.model.encode(self.words, show_progress_bar=False)
        
        for word, vector in zip(self.words, vectors):
            self.word_vectors[word] = vector
        
        # Save cache
        with open(cache_file, 'wb') as f:
            pickle.dump({
                'words': self.words,
                'vectors': self.word_vectors
            }, f)
        
        print("Indexing complete! Cached for next time.")
    
    def semantic_search(self, query, top_k=5):
        if not self.word_vectors:
            return []
        
        query_vector = self.model.encode([query], show_progress_bar=False)[0]
        
        similarities = []
        for word, vector in self.word_vectors.items():
            sim = np.dot(query_vector, vector) / (np.linalg.norm(query_vector) * np.linalg.norm(vector))
            similarities.append((word, sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:top_k]