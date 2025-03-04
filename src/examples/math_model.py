def profit(
        n: int, # number of prompts
        p: float, # hit rate
        c_e: float, # price of embedding tokens
        c_q: float, # price of request tokens
        t_input: int, # token amount for input
        t_output: int, # token amount for output
    ) -> float:
    return n * (p * c_q * (t_input + t_output) - c_e * t_input)


def main():
# {
#   "total_prompts": 50,
#   "cache_hits": 19,
#   "tokens_with_cache": 6640,
#   "tokens_without_cache": 9197,
#   "price_with_cache": 0.011727699999999994,
#   "price_without_cache": 0.018393999999999997,
#   "price_saved_percent": 36.24170925301732,
#   "avg_response_time": 0.1727653217315674,
#   "total_time": 8.63826608657837,
#   "cache_hit_rate": 0.38,
#   "avg_prompt_tokens": 16.34,
#   "avg_response_tokens": 167.6,
#   "max_prompt_tokens": 26,
#   "max_response_tokens": 220
# }
    # Тестовые сценарии с реальными ценами OpenAI
    scenarios = [
        {
            "name": "Реальный тест",
            "params": {
                "n": 50,
                "p": 0.38,
                "c_e": 0.001 / 1000,  # $0.0001 per 1K tokens для embedding
                "c_q": 0.02 / 1000,   # $0.002 per 1K tokens для GPT-3.5
                "t_input": 16.34,       # средняя длина промпта
                "t_output": 167.6      # средняя длина ответа
            }
        },
        {
            "name": "Длинные промпты",
            "params": {
                "n": 50,
                "p": 0.38,
                "c_e": 0.0001/1000,
                "c_q": 0.002/1000,
                "t_input": 1000,    # длинный промпт
                "t_output": 2000    # длинный ответ
            }
        },
        {
            "name": "Высокий hit rate",
            "params": {
                "n": 50,
                "p": 0.9,          # высокий процент попаданий в кэш
                "c_e": 0.0001/1000,
                "c_q": 0.002/1000,
                "t_input": 16,
                "t_output": 167
            }
        }
    ]
    
    for scenario in scenarios:
        params = scenario["params"]
        savings = profit(**params)
        print(f"\nСценарий: {scenario['name']}")
        print(f"Экономия: ${savings:.6f}")
        print(f"Экономия на 1M запросов: ${savings/params['n']*1_000_000:.2f}")
        
        # Добавим подробный анализ затрат
        n = params["n"]
        cost_without = n *(params["t_input"] + params["t_output"])
        embed_cost = n * params["t_input"]
        request_cost = (1-params["p"]) * n * (params["t_input"] + params["t_output"])
        print(f"Анализ затрат токенов:")
        print(f"- Без кэша: {cost_without}")
        print(f"- С кэшем (эмбеддинги): {embed_cost}")
        print(f"- С кэшем (запросы): {request_cost:.1f}")
        print(f"- Общие затраты с кэшем: {(embed_cost + request_cost)}")

if __name__ == "__main__":
    main()