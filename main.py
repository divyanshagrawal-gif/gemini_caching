# main.py or wherever you use the cache
from layered_cache import layered_cache
from langchain_core.globals import set_llm_cache
from LLM import llm
import time

# Set the layered cache as the global cache
set_llm_cache(layered_cache)

def execute_with_time(prompt):
    start_time = time.time()
    result = llm.invoke(prompt)
    end_time = time.time()
    return result.text, end_time - start_time

# Test the layered cache
print('Executing first time...')
result, time_taken = execute_with_time("What is the capital city of France?")
print(result)
print(f"Time taken: {time_taken} seconds")

print('\nExecuting second time (exact match - should hit L1)...')
result, time_taken2 = execute_with_time("What is the capital city of France?")
print(result)
print(f"Time taken: {time_taken2} seconds")

print('\nExecuting third time (semantic similarity - should hit L2, then promote to L1)...')
result, time_taken3 = execute_with_time("CAN YOU TELL ME THE CAPITAL CITY OF FRANCE?")
print(result)
print(f"Time taken: {time_taken3} seconds")

print(f"\nL1 speedup: {time_taken/time_taken2:.2f}x faster")
print(f"L2 speedup: {time_taken/time_taken3:.2f}x faster")