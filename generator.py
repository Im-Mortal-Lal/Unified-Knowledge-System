from langchain_ollama import ChatOllama

from config import *
from prompts import build_prompt

llm = ChatOllama(
    model=LLM_MODEL
)


def generate_answer(context, query):

    prompt = build_prompt(
        context,
        query
    )

    response = llm.invoke(prompt)

    if hasattr(response, "content"):
        return response.content

    return response