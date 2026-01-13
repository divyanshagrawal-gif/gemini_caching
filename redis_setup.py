from redis import Redis
from dotenv import load_dotenv
import os
from langchain_redis import RedisCache
from langchain_redis import RedisSemanticCache
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
redis_url = os.getenv("REDIS_URL")
# redis_client = Redis.from_url(redis_url)
# print(redis_client.ping())   # to check if the redis is connected

# L1 Cache with TTL
redis_cache = RedisCache(
    redis_url=redis_url,
    ttl=3600,  # 1 hour
    prefix="l1_cache"
)

# L2 Cache with Semantic Similarity
smenatic_cache = RedisSemanticCache(
    redis_url = redis_url, 
    embeddings=embeddings, 
    distance_threshold=0.2,
    prefix="l2_cache",  # to avoid conflicts with the l1 cache
    ttl=7200  # 2 hours
)
