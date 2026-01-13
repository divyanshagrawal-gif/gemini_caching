from redis_setup import redis_cache
from LLM import llm
from langchain_core.globals import set_llm_cache
import time



set_llm_cache(redis_cache)

def execute_with_time(prompt):
    start_time = time.time()
    result = llm.invoke(prompt)
    end_time = time.time()
    return result.text, end_time - start_time

print('Executing first time...')
result, time_taken = execute_with_time("Hello, how are you?")
print(result)
print(f"Time taken: {time_taken} seconds")

print('Executing second time...')
result, time_taken2 = execute_with_time("Hello, how are you?")
print(result)
print(f"Time taken: {time_taken2} seconds")

print(f"speedup: {time_taken/time_taken2:.2f}x faster")
