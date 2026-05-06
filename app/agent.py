try:
    from langchain.memory import ConversationBufferMemory
except ImportError:  # Allows running the agent before dependencies are installed.
    ConversationBufferMemory = None


QUESTIONS = [
    "¿Cuál es tu nombre?",
    "¿Cuántos años tienes?",
    "¿Cuál es tu objetivo principal: perder peso, ganar músculo o mejorar resistencia?",
]

WELCOME_MESSAGE = f"¡Hola! Bienvenido a WellTrack. {QUESTIONS[0]}"


def get_next_question(step: int) -> str | None:
    if step < len(QUESTIONS):
        return QUESTIONS[step]
    return None


def generate_summary(data: dict) -> str:
    return (
        "Resumen del usuario:\n"
        f"- Nombre: {data.get('name')}\n"
        f"- Edad: {data.get('age')}\n"
        f"- Objetivo: {data.get('goal')}"
    )


class WellTrackAgent:
    """Deterministic LangChain-backed onboarding flow for independent testing."""

    def __init__(self):
        self.step = -1
        self.data = {"name": "", "age": "", "goal": ""}
        self.is_final = False
        self.memory = (
            ConversationBufferMemory(return_messages=True)
            if ConversationBufferMemory is not None
            else None
        )
        self.history = []

    def _remember(self, user_message: str, agent_response: str) -> None:
        if self.memory is not None:
            self.memory.save_context(
                {"input": user_message},
                {"output": agent_response},
            )
        else:
            self.history.append({"user": user_message, "agent": agent_response})

    def invoke(self, message: str) -> dict:
        if self.is_final:
            response = "La sesión ya finalizó."
            return {"response": response, "is_final": True, "summary": generate_summary(self.data)}

        if self.step == -1:
            self.step = 0
            response = WELCOME_MESSAGE
            self._remember(message, response)
            return {"response": response, "is_final": False, "summary": None}

        if self.step == 0:
            self.data["name"] = message
        elif self.step == 1:
            self.data["age"] = message
        elif self.step == 2:
            self.data["goal"] = message

        self.step += 1

        if self.step == len(QUESTIONS):
            self.is_final = True
            summary = generate_summary(self.data)
            response = "Gracias, hemos terminado tu onboarding."
            self._remember(message, response)
            return {"response": response, "is_final": True, "summary": summary}

        response = get_next_question(self.step)
        self._remember(message, response)
        return {"response": response, "is_final": False, "summary": None}


if __name__ == "__main__":
    agent = WellTrackAgent()
    print(agent.invoke("hola"))
    print(agent.invoke("Juan"))
    print(agent.invoke("25"))
    print(agent.invoke("ganar músculo"))
