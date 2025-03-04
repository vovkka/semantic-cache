from src.base.abstract_cache import AbstractSemanticCache
from src.local_embeddings import LocalSentenceTransformer
from src.examples.mock import MockPromptClient
from src.utils.prompt_generator import PromptGenerator
import tiktoken
import time
from typing import Dict, List
import json

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Подсчет количества токенов в тексте
    """
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def run_benchmark(prompts: List[str], cache: AbstractSemanticCache) -> Dict:
    c_e = 0.0001/1000
    c_q = 0.002/1000

    total_tokens_with_cache = 0
    total_tokens_without_cache = 0
    total_price_with_cache = 0
    total_price_without_cache = 0
    cache_hits = 0
    times = []
    prompt_tokens_list = []
    response_tokens_list = []
    
    for prompt in prompts:
        start_time = time.time()
        response, is_cache_hit = cache.get_response(prompt)
        times.append(time.time() - start_time)
        
        prompt_tokens = count_tokens(prompt)
        response_tokens = count_tokens(response)
        prompt_tokens_list.append(prompt_tokens)
        response_tokens_list.append(response_tokens)
        total_price_without_cache += prompt_tokens * c_q + response_tokens * c_q
        total_tokens_without_cache += prompt_tokens + response_tokens
        
        if is_cache_hit:
            cache_hits += 1
            total_tokens_with_cache += prompt_tokens
            total_price_with_cache += c_e * prompt_tokens
        else:
            total_tokens_with_cache += prompt_tokens + response_tokens + prompt_tokens
            total_price_with_cache += prompt_tokens * c_q + response_tokens * c_q + c_e * prompt_tokens
    
    return {
        "total_prompts": len(prompts),
        "cache_hits": cache_hits,
        "tokens_with_cache": total_tokens_with_cache,
        "tokens_without_cache": total_tokens_without_cache,
        "price_with_cache": total_price_with_cache,
        "price_without_cache": total_price_without_cache,
        "price_saved_percent": (1 - total_price_with_cache / total_price_without_cache) * 100,
        "avg_response_time": sum(times) / len(times),
        "total_time": sum(times),
        "cache_hit_rate": cache_hits / len(prompts),
        "avg_prompt_tokens": sum(prompt_tokens_list) / len(prompt_tokens_list),
        "avg_response_tokens": sum(response_tokens_list) / len(response_tokens_list),
        "max_prompt_tokens": max(prompt_tokens_list),
        "max_response_tokens": max(response_tokens_list)
    }

def main():
    # Инициализация компонентов
    generator = PromptGenerator()
    cache = AbstractSemanticCache(
        embedding_model=LocalSentenceTransformer(),
        prompt_client=MockPromptClient(delay_range=(0.1, 0.3))
    )
    
    # Генерация тестовых промптов
    base_prompts = generator.generate_prompts(count=10, seed=42)
    all_prompts = []
    
    # Для каждого базового промпта генерируем похожие
    for prompt in base_prompts:
        variations = generator.generate_similar_prompts(prompt, variations=5)
        all_prompts.extend(variations)
    
    # Запуск тестирования
    results = run_benchmark(all_prompts, cache)
    
    # Вывод результатов
    print("\nРезультаты тестирования:")
    print(json.dumps(results, indent=2, ensure_ascii=False))
    
    print(f"\nЭкономия токенов: {(1 - results['tokens_with_cache']/results['tokens_without_cache'])*100:.1f}%")
    print(f"Экономия денег: {results['price_saved_percent']:.1f}%")
    print(f"Процент попаданий в кэш: {results['cache_hit_rate']*100:.1f}%")
    print(f"Среднее время ответа: {results['avg_response_time']*1000:.0f}ms")
    print(f"Средняя длина промпта: {results['avg_prompt_tokens']:.1f} токенов")
    print(f"Средняя длина ответа: {results['avg_response_tokens']:.1f} токенов")
    print(f"Максимальная длина промпта: {results['max_prompt_tokens']} токенов")
    print(f"Максимальная длина ответа: {results['max_response_tokens']} токенов")

if __name__ == "__main__":
    main()
