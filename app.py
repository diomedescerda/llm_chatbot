from openai import OpenAI
import os
from dotenv import load_dotenv
import gradio as gr

load_dotenv()
gemini_key = os.environ.get("GEMINI_API_KEY")
open_router_key = os.environ.get("OPENROUTER_API_KEY")

open_router = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=open_router_key)
gemini = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=gemini_key)

ollama = OpenAI(base_url='http://localhost:11434/v1', api_key='ollama')
model_name = "gpt-oss:20b"

def chat(message, history, provider, model, task):
    try:
        system_messages = []
        if task == "Traducción":
            system_messages.append({
                "role": "system",
                "content": "Eres un traductor, debes traducir todo al idioma Español.",
            })
        elif task == "Resumen":
            system_messages.append({
                "role": "system",
                "content": "Eres un asistente que realiza resumenes de textos.",
            })
        else:
            system_messages.extend([
                {
                    "role": "system",
                    "content": "Eres un traductor, debes traducir todo al idioma Español.",
                },
                {
                    "role": "system",
                    "content": "Eres un asistente que realiza resumenes de textos.",
                }
            ])

        for msg in history:
            if msg["role"] == "user":
                system_messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == "assistant":
                system_messages.append({"role": "assistant", "content": msg["content"]})

        system_messages.append({"role": "user", "content": message})

        if provider == "OpenRouter":
            client = open_router
            model_name = model  # Use the full model name for OpenRouter
        elif provider == "Google":
            client = gemini
            model_name = f"models/{model}"  # Add models/ prefix for Gemini
        elif provider == "Ollama":
            client = ollama
            model_name = model
        else:
            raise ValueError(f"Unsupported provider: {provider}")

        resp = client.chat.completions.create(
            model=model_name,
            messages=system_messages,
        )
        return resp.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"

if __name__ == "__main__":

    PROVIDERS = ["OpenRouter", "Google", "Ollama"]
    MODELS = {
        "OpenRouter": ["deepseek/deepseek-chat-v3.1:free"],
        "Google": ["gemini-2.5-flash-lite"],
        "Ollama": ["gpt-oss:20b"],
    }
    TASKS = ["Traducción", "Resumen"]

    def update_models(provider):
        return gr.Dropdown(choices=MODELS[provider], value=MODELS[provider][0])

    def chat_with_config(message, history, provider, model, task):
        return chat(message, history, provider, model, task)

    with gr.Blocks() as demo:
        gr.Markdown("## LLMs Chatbot")
            
        with gr.Row():
            provider = gr.Dropdown(PROVIDERS, label="Provider", value=PROVIDERS[0])
            model = gr.Dropdown(MODELS[PROVIDERS[0]], label="Model", value=MODELS[PROVIDERS[0]][0])
            task = gr.Dropdown(TASKS, label="Task", value=TASKS[0])
        
        provider.change(update_models, provider, model)
        
        chatbot = gr.ChatInterface(
            fn=chat_with_config,
            additional_inputs=[provider, model, task],
            type="messages"
        )
    
    demo.launch()