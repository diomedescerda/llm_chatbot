# llm_chatbot

Este proyecto es un chatbot basado en acceso por medio de keys a LLMs (Large Language Model) usando la libreria de OpenAI.

## Instalación

1. Clona el repositorio:
   ```
   git clone https://github.com/diomedescerda/llm_chatbot.git
   ```
2. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Uso

Ejecuta la aplicación:
```
python app.py
```

## Configuración

Asegúrate de tener las keys en variables de entorno llamadas `GEMINI_API_KEY` y `OPENROUTER_API_KEY`.
Además de esto, el modelo especifico de Ollama que se usa, en este caso por defecto es `gpt-oss:20b`.

## Estructura
- `app.py`: Código principal del chatbot.
- `requirements.txt`: Dependencias del proyecto.