from openai import OpenAI
from app.config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


QUESTIONS = [
    "¿Cuál es tu nombre?",
    "¿Cuántos años tienes?",
    "¿Cuál es tu objetivo principal: perder peso, ganar músculo o mejorar resistencia?"
]


def generate_summary(data: dict) -> str:
    return (
        f"Resumen del usuario:\n"
        f"- Nombre: {data.get('name')}\n"
        f"- Edad: {data.get('age')}\n"
        f"- Objetivo: {data.get('goal')}"
    )


def get_next_question(step: int):
    if step < len(QUESTIONS):
        return QUESTIONS[step]
    return None