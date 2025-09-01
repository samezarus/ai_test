# pip install -U langgraph langchain langchain-community langchain-ollama ddgs


# main.py
from langchain_ollama import ChatOllama
from langchain_community.tools import DuckDuckGoSearchRun
from langgraph.prebuilt import create_react_agent

# 1. Чат-модель Ollama
# model = ChatOllama(model="gpt-oss:20b")
# model = ChatOllama(model="qwen3:32b")
model = ChatOllama(model="gemma3:27b")

# 2. Инструмент поиска в интернете
search = DuckDuckGoSearchRun()

# 3. Агент в стиле ReAct на LangGraph
agent = create_react_agent(
    model=model,
    tools=[search],
)

# 4. Запуск
if __name__ == "__main__":
    query = """
    - Ты AI агент по поиску информации в интернете, который не придумывает и недодумывает.
    - Думай и отвечай на русском языке.
    - Ссылки на источники должны вести на реальные свйты.
    - Найди свежие новости про open-source LLM в 2025 году.
    """

    print("=== STREAM ===")
    for step in agent.stream({"messages": [("user", query)]}):
        print(step)

    print("\n=== ФИНАЛЬНЫЙ ОТВЕТ ===")
    result = agent.invoke({"messages": [("user", query)]})
    print(result["messages"][-1].content)

    with open("result.md", "w", encoding="utf-8") as f:
        f.write(result["messages"][-1].content)