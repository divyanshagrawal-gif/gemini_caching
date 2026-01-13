# layered_cache.py
from typing import Optional, Any
from langchain_core.caches import BaseCache
from redis_setup import redis_cache, smenatic_cache


class LayeredCache(BaseCache):
    """
    A layered cache that checks L1 (exact match) first, then L2 (semantic similarity).
    """
    
    def __init__(self, l1_cache, l2_cache):
        self.l1_cache = l1_cache  # RedisCache (exact match)
        self.l2_cache = l2_cache  # RedisSemanticCache (semantic similarity)
    
    def lookup(self, prompt: str, llm_string: str) -> Optional[Any]:
        """
        Check L1 cache first, then L2 cache.
        Returns the cached result if found, None otherwise.
        """
        # Check L1 cache (exact match) first
        result = self.l1_cache.lookup(prompt, llm_string)
        if result is not None:
            print("✅ L1 Cache HIT (exact match)")
            return result
        
        # If L1 misses, check L2 cache (semantic similarity)
        result = self.l2_cache.lookup(prompt, llm_string)
        if result is not None:
            print("✅ L2 Cache HIT (semantic similarity)")
            # Promote to L1 cache for faster future access
            self.l1_cache.update(prompt, llm_string, result)
            return result
        
        print("❌ Cache MISS (both L1 and L2)")
        return None
    
    def update(self, prompt: str, llm_string: str, return_val: Any) -> None:
        """
        Update both L1 and L2 caches when there's a cache miss.
        """
        # Update L1 cache (exact match)
        self.l1_cache.update(prompt, llm_string, return_val)
        # Update L2 cache (semantic similarity)
        self.l2_cache.update(prompt, llm_string, return_val)
        print("💾 Updated both L1 and L2 caches")

    def clear(self) -> None:
        """
        Clear both L1 and L2 caches.
        """
        if hasattr(self.l1_cache, 'clear'):
            self.l1_cache.clear()
        if hasattr(self.l2_cache, 'clear'):
            self.l2_cache.clear()
        print("🗑️  Cleared both L1 and L2 caches")


layered_cache = LayeredCache(
    l1_cache=redis_cache,  # From redis_setup
    l2_cache=smenatic_cache
)