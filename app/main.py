from fastapi import FastAPI
from app.schemas import ChatRequest, ChatResponse
from app.memory import sessions
from app.agent import QUESTIONS, get_next_question, generate_summary

app = FastAPI()


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    session_id = request.session_id
    message = request.message

    # inicializar sesión si no existe
    if session_id not in sessions:
        sessions[session_id] = {
            "step": 0,
            "name": "",
            "age": "",
            "goal": ""
        }

    session = sessions[session_id]

    step = session["step"]

    # guardar respuesta anterior
    if step == 0:
        session["name"] = message
    elif step == 1:
        session["age"] = message
    elif step == 2:
        session["goal"] = message

    session["step"] += 1

    # verificar si terminó
    if session["step"] >= len(QUESTIONS):

        summary = generate_summary(session)

        return ChatResponse(
            response="Gracias, hemos terminado tu onboarding.",
            is_final=True,
            summary=summary
        )

    # siguiente pregunta
    next_q = get_next_question(session["step"])

    return ChatResponse(
        response=next_q,
        is_final=False,
        summary=None
    )