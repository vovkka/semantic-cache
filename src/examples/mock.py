from src.base.abstract_cache import PromptClient
import random
import time

class MockPromptClient(PromptClient):
    """Мок-клиент для тестирования без использования API"""
    
    def __init__(self, delay_range: tuple[float, float] = (0.1, 0.5)):
        self.responses = {
            "programming": [
                "Python - высокоуровневый язык программирования..." * 10,
                "JavaScript используется для веб-разработки..." * 10,
                "Java является одним из самых популярных языков..." * 10,
            ],
            "science": [
                "Квантовая механика описывает поведение материи..." * 10,
                "Теория относительности Эйнштейна утверждает..." * 10,
                "Химические реакции происходят при взаимодействии..." * 10,
            ],
            "other": [
                "Это интересный вопрос, который требует рассмотрения..." * 10,
                "Давайте разберем этот вопрос подробнее..." * 10,
                "Существует несколько подходов к решению..." * 10,
            ]
        }
        self.delay_range = delay_range
    
    def get_completion(self, prompt: str) -> str:
        # Имитация задержки API
        time.sleep(random.uniform(*self.delay_range))
        
        # Простая логика выбора ответа на основе ключевых слов
        if any(word in prompt.lower() for word in ["python", "программирование", "код"]):
            category = "programming"
        elif any(word in prompt.lower() for word in ["физика", "химия", "наука"]):
            category = "science"
        else:
            category = "other"
            
        return random.choice(self.responses[category])
