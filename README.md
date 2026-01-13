# Gemini Caching - Layered Cache System

A two-tier caching system for Google Gemini LLM responses using Redis, implementing both exact match (L1) and semantic similarity (L2) caching layers.

## Architecture

The system implements a **layered cache architecture**:

- **L1 Cache (RedisCache)**: Fast exact string matching with shorter TTL (1 hour)
- **L2 Cache (RedisSemanticCache)**: Semantic similarity matching with longer TTL (2 hours)
- **Cache Promotion**: L2 hits are automatically promoted to L1 for faster future access

### How It Works

1. **First Request**: Query L1 → Miss → Query L2 → Miss → Call LLM → Store in both L1 & L2
2. **Exact Match**: Query L1 → Hit → Return cached result
3. **Semantic Match**: Query L1 → Miss → Query L2 → Hit → Promote to L1 → Return cached result

## Setup

### Prerequisites

- Python 3.12+
- Redis server running
- Google Gemini API key

### Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:
   Create a `.env` file:
   ```env
   REDIS_URL=redis://localhost:6379
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```

3. **Start Redis** (if not already running):
   ```bash
   redis-server
   ```

## Project Structure

```
.
├── LLM.py              # Google Gemini LLM configuration
├── redis_setup.py      # L1 and L2 cache setup (RedisCache + RedisSemanticCache)
├── layered_cache.py    # Layered cache wrapper implementation
├── main.py             # Main execution with layered cache
├── L1_cache.py         # Standalone L1 cache example
├── L2_cache.py         # Standalone L2 cache example
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## Usage

### Using Layered Cache (Recommended)

```python
from layered_cache import layered_cache
from langchain_core.globals import set_llm_cache
from LLM import llm

# Set layered cache
set_llm_cache(layered_cache)

# Use LLM - caching happens automatically
result = llm.invoke("What is the capital of France?")
```

### Running the Example

```bash
python main.py
```

This will demonstrate:
- First execution (cache miss)
- Exact match cache hit (L1)
- Semantic similarity cache hit (L2)

### Standalone Cache Examples

You can also test individual cache layers:

```bash
# Test L1 cache only (exact matching)
python L1_cache.py

# Test L2 cache only (semantic similarity)
python L2_cache.py
```

## Configuration

### Cache TTL (Time To Live)

Configure TTL in `redis_setup.py`:

```python
# L1 Cache - Shorter TTL for faster refresh
redis_cache = RedisCache(
    redis_url=redis_url,
    ttl=3600,  # 1 hour
    prefix="l1_cache"
)

# L2 Cache - Longer TTL for persistence
smenatic_cache = RedisSemanticCache(
    redis_url=redis_url,
    embeddings=embeddings,
    distance_threshold=0.2,
    ttl=7200,  # 2 hours
    prefix="l2_cache"
)
```

### Semantic Similarity Threshold

Adjust `distance_threshold` in `redis_setup.py`:
- **Lower values (0.1-0.2)**: Stricter matching, fewer false positives
- **Higher values (0.3-0.5)**: More lenient matching, more cache hits

```python
smenatic_cache = RedisSemanticCache(
    redis_url=redis_url,
    embeddings=embeddings,
    distance_threshold=0.2,  # Default: 0.2
    prefix="l2_cache",
    ttl=7200
)
```

### Redis Eviction Policy

Configure at Redis server level:

```bash
# Set max memory
redis-cli CONFIG SET maxmemory 2gb

# Set eviction policy (e.g., LRU)
redis-cli CONFIG SET maxmemory-policy allkeys-lru
```

Or create a `redis.conf` file:
```conf
maxmemory 2gb
maxmemory-policy allkeys-lru
```

## Components

### `redis_setup.py`

Central configuration file that sets up both cache layers:
- **L1 Cache (`redis_cache`)**: `RedisCache` for exact string matching
- **L2 Cache (`smenatic_cache`)**: `RedisSemanticCache` for semantic similarity
- **Embeddings**: Google Gemini embeddings model configuration

### `LayeredCache` Class

Implements `BaseCache` interface with:
- `lookup()`: Checks L1, then L2, with automatic promotion
- `update()`: Updates both caches on miss
- `clear()`: Clears both cache layers

The class wraps the caches from `redis_setup.py` to provide a unified interface.

### Cache Types

- **L1 (RedisCache)**: Exact string matching using MD5 hashes
- **L2 (RedisSemanticCache)**: Vector similarity search using embeddings

## Dependencies

- `langchain-google-genai`: Google Gemini integration
- `langchain-redis`: Redis caching backends
- `langchain-core`: Core LangChain functionality
- `redis`: Redis Python client
- `python-dotenv`: Environment variable management

## Performance

The layered cache provides:
- **L1 Hit**: ~10-100x faster than LLM call
- **L2 Hit**: ~5-50x faster than LLM call (includes embedding lookup)
- **Cache Promotion**: L2 hits are stored in L1 for instant future access

## Notes

- L1 cache uses exact matching - same prompt = instant hit
- L2 cache uses semantic similarity - similar prompts = cache hit
- Both caches are updated on every miss to maximize future hits
- TTL ensures cache freshness and prevents stale data
