# pip install ollama
import pprint

import ollama
import sys
import json
import base64
import re

def analyze_image(_file_path: str) -> dict:
    """
    Отправляет изображение в Ollama (llava), извлекает текст и делает саммари.
    Возвращает dict с полями {"text": "...", "summary": "..."}.
    """

    # Загружаем и кодируем картинку в base64
    with open(_file_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

#     prompt = """
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

    response = ollama.generate(
        # model="qwen2.5vl:3b",
        # model="qwen2.5vl:7b",
        model="qwen2.5vl:32b",
        prompt=prompt,
        images=[image_base64],
        stream=False
    )

    return response


if __name__ == "__main__":
    file_path = "./skan.jpg"
    # file_path = "./1.pdf"

    result = analyze_image(file_path)

    print(result.response)

    with open("example.md", "w", encoding="utf-8") as f:
        f.write(result.response)
