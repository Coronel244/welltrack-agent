from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app.agent import QUESTIONS, WELCOME_MESSAGE, generate_summary, get_next_question
from app.memory import sessions
from app.schemas import ChatRequest, ChatResponse

app = FastAPI(title="WellTrack Agent")


@app.exception_handler(Exception)
def global_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "response": "Error interno del servidor",
            "is_final": False,
            "summary": None,
        },
    )


def _validate_request(request: ChatRequest) -> tuple[str, str]:
    session_id = request.session_id.strip()
    message = request.message.strip()

    if not session_id or not message:
        raise HTTPException(
            status_code=400,
            detail="session_id y message son obligatorios",
        )

    return session_id, message


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    session_id, message = _validate_request(request)

    if session_id not in sessions:
        sessions[session_id] = {
            "step": 0,
            "name": "",
            "age": "",
            "goal": "",
        }

        return ChatResponse(
            response=WELCOME_MESSAGE,
            is_final=False,
            summary=None,
        )

    session = sessions[session_id]
    step = session["step"]

    if step == 0:
        session["name"] = message
    elif step == 1:
        if not message.isdigit():
            return ChatResponse(
                response="Por favor ingresa una edad válida (número).",
                is_final=False,
                summary=None,
            )
        session["age"] = message
    elif step == 2:
        session["goal"] = message

    session["step"] += 1

    if session["step"] == len(QUESTIONS):
        summary = generate_summary(session)
        del sessions[session_id]

        return ChatResponse(
            response="Gracias, hemos terminado tu onboarding.",
            is_final=True,
            summary=summary,
        )

    next_q = get_next_question(session["step"])

    return ChatResponse(
        response=next_q,
        is_final=False,
        summary=None,
    )
