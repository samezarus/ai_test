# pip install langchain langchain-community ollama
# pip install langchain-ollama
# pip install langchain-core


import base64
from langchain.chat_models import ChatOpenAI  # или аналогичный класс
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage
from pathlib import Path

# кодируем изображение
img_bytes = Path("skan.jpg").read_bytes()
img_b64 = base64.b64encode(img_bytes).decode("utf-8")

# prompt = """
# # Ты мультимодальный AI-агент для работы со сканированными документами на русском языке.
# # Задача: проанализировать изображение и вернуть данные в формате JSON со следующими ключами:
# - text: извлечённый текст (или пустая строка, если текста нет)
# - summary: краткое содержание текста (или пустая строка, если текста нет)
# - tables: список таблиц в markdown-нотации (или пустой массив, если таблиц нет)
# # Замечания:
# - Не придумывай данные, если не смог распознать их на изображении
# - Соблюдай чёткую последовательность данных в тексте
# """

prompt = """
# Ты мультимодальный AI-агент для работы со сканированными документами на русском языке.  
## Задача: 
- Проанализировать изображение и вернуть данные
## Возвращаемые данные:
- Весь извлечённый текст
- Таблица в markdown-нотации
## Замечания:
- Не проверяй орфографию и правописание
- Соблюдай чёткую последовательность данных в тексте и таблицах
- Не придумывай данные, если не смог распознать их на изображении
"""

message = HumanMessage(
    content=[
        {
            "type": "text", 
            "text": prompt
        },
        {
            "type": "image", 
            "source_type": "base64", 
            "mime_type": "image/jpg", 
            "data": img_b64
        },
    ]
)

llm = ChatOllama(
    # model="qwen2.5vl:3b",
    # model="qwen2.5vl:7b",
    model="qwen2.5vl:32b",
    base_url="http://localhost:11434"
)

response = llm.invoke([message])
print(response.content)
