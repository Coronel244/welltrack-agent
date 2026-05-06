# WellTrack Agent

Agente conversacional simple para onboarding de usuarios de WellTrack. El flujo hace siempre las mismas 3 preguntas en orden:

1. ¿Cuál es tu nombre?
2. ¿Cuántos años tienes?
3. ¿Cuál es tu objetivo principal: perder peso, ganar músculo o mejorar resistencia?

Al terminar, el endpoint devuelve `is_final: true` y un resumen con los datos capturados.

## Arquitectura

- `app/agent.py`: flujo del agente, preguntas, resumen y prueba independiente.
- `app/main.py`: API FastAPI con endpoint `POST /chat`.
- `app/memory.py`: sesiones en memoria RAM por `session_id`.
- `app/schemas.py`: modelos Pydantic de request y response.

## Ejecutar

```bash
pip install -r requirements.txt
copy .env.example .env
python run.py
```

La API queda disponible en:

```text
http://127.0.0.1:8000
```

Variable de entorno requerida en `.env`:

```env
OPENAI_API_KEY=tu_api_key_aqui
```

## Probar el agente sin API

```bash
python -m app.agent
```

## Pruebas con curl en Windows CMD

Paso 1: inicia la sesión y pregunta el nombre.

```cmd
curl -X POST http://127.0.0.1:8000/chat ^
-H "Content-Type: application/json" ^
-d "{\"session_id\":\"user_1\",\"message\":\"hola\"}"
```

Respuesta esperada:

```json
{
  "response": "¡Hola! Bienvenido a WellTrack. ¿Cuál es tu nombre?",
  "is_final": false,
  "summary": null
}
```

Paso 2: guarda el nombre y pregunta la edad.

```cmd
curl -X POST http://127.0.0.1:8000/chat ^
-H "Content-Type: application/json" ^
-d "{\"session_id\":\"user_1\",\"message\":\"Juan\"}"
```

Respuesta esperada:

```json
{
  "response": "¿Cuántos años tienes?",
  "is_final": false,
  "summary": null
}
```

Paso 3: guarda la edad y pregunta el objetivo.

```cmd
curl -X POST http://127.0.0.1:8000/chat ^
-H "Content-Type: application/json" ^
-d "{\"session_id\":\"user_1\",\"message\":\"25\"}"
```

Respuesta esperada:

```json
{
  "response": "¿Cuál es tu objetivo principal: perder peso, ganar músculo o mejorar resistencia?",
  "is_final": false,
  "summary": null
}
```

Paso 4: guarda el objetivo y finaliza.

```cmd
curl -X POST http://127.0.0.1:8000/chat ^
-H "Content-Type: application/json" ^
-d "{\"session_id\":\"user_1\",\"message\":\"ganar músculo\"}"
```

Respuesta esperada:

```json
{
  "response": "Gracias, hemos terminado tu onboarding.",
  "is_final": true,
  "summary": "Resumen del usuario:\n- Nombre: Juan\n- Edad: 25\n- Objetivo: ganar músculo"
}
```

## Validaciones

- `session_id` no puede estar vacío.
- `message` no puede estar vacío.
- La edad debe ser numérica.
