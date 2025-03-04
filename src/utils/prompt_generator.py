import random
from typing import List, Optional

class PromptGenerator:
    """Генератор тестовых промптов"""
    
    def __init__(self):
        self.templates = {
            "programming": [
                "Расскажи про язык программирования {language}",
                "Как научиться программировать на {language}?",
                "Сравни {language} и {language2}",
                "Что лучше для {task}: {language} или {language2}?",
            ],
            "science": [
                "Объясни концепцию {concept} в {field}",
                "Как работает {concept}?",
                "Почему {concept} важен в {field}?",
                "Расскажи о применении {concept} в {field}",
            ]
        }
        
        self.data = {
            "language": ["Python", "JavaScript", "Java", "C++", "Ruby", "Go"],
            "task": ["веб-разработки", "анализа данных", "машинного обучения", "разработки игр"],
            "concept": ["квантовая механика", "гравитация", "энтропия", "химическая связь"],
            "field": ["физике", "химии", "биологии", "астрономии"]
        }
    
    def generate_prompts(self, count: int, seed: Optional[int] = None) -> List[str]:
        """Генерирует список промптов"""
        if seed is not None:
            random.seed(seed)
            
        prompts = []
        for _ in range(count):
            category = random.choice(list(self.templates.keys()))
            template = random.choice(self.templates[category])
            
            # Заполняем шаблон случайными значениями
            prompt = template
            for key in self.data.keys():
                if "{" + key + "}" in prompt:
                    prompt = prompt.replace("{" + key + "}", random.choice(self.data[key]))
                if "{" + key + "2}" in prompt:
                    # Для сравнения выбираем другой язык
                    second = random.choice([x for x in self.data[key] if x not in prompt])
                    prompt = prompt.replace("{" + key + "2}", second)
            
            prompts.append(prompt)
            
        return prompts

    def generate_similar_prompts(self, base_prompt: str, variations: int) -> List[str]:
        """Генерирует вариации заданного промпта"""
        words = base_prompt.split()
        prompts = [base_prompt]
        
        for _ in range(variations - 1):
            # Создаем вариацию, изменяя или переставляя слова
            new_words = words.copy()
            
            # Выбираем случайное преобразование
            transform = random.choice(['rephrase', 'reorder'])
            
            if transform == 'rephrase':
                # Заменяем некоторые слова синонимами или близкими по смыслу
                replacements = {
                    'расскажи': ['объясни', 'опиши', 'поведай'],
                    'про': ['о', 'об'],
                    'язык': ['язык программирования'],
                    'как': ['каким образом', 'какими способами'],
                    'научиться': ['изучить', 'освоить', 'выучить'],
                }
                
                for i, word in enumerate(new_words):
                    if word.lower() in replacements:
                        new_words[i] = random.choice(replacements[word.lower()])
            
            else:  # reorder
                # Переставляем части предложения
                if len(new_words) > 3:
                    split = random.randint(1, len(new_words)-2)
                    new_words = new_words[split:] + new_words[:split]
            
            prompts.append(' '.join(new_words))
        
        return prompts
