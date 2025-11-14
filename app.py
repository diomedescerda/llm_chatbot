from openai import OpenAI
import os
from dotenv import load_dotenv
import gradio as gr
import mlflow
import time

mlflow.set_tracking_uri("http://mlflow-server:5000")
mlflow.set_experiment("translation_app") 

load_dotenv()
gemini_key = os.environ.get("GEMINI_API_KEY")
open_router_key = os.environ.get("OPENROUTER_API_KEY")

open_router = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=open_router_key)
gemini = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key=gemini_key)

def chat(message, history, provider, model, target_language):
    start_time =  time.time()

    prompt = (
        f"Traduce el siguiente texto al idioma {target_language}. "
        "Devuelve solo la traducción, sin explicaciones.\n\n"
        f"Texto:\n{message}\n\nTraducción:"
    )

    if provider == "OpenRouter":
        client = open_router
        model_name = model
    elif provider == "Google":
        client = gemini
        model_name = f"models/{model}"
    else:
        raise ValueError(f"Unsupported provider: {provider}")

    resp = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
    )
    translated = resp.choices[0].message.content
    
    # Metrics
    latency = time.time() - start_time
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    with mlflow.start_run(run_name=f"{provider}_{model}_{target_language}"):
        mlflow.log_param("provider", provider)
        mlflow.log_param("model", model_name)
        mlflow.log_param("target_language", target_language)
        mlflow.log_param("timestamp", timestamp)

        mlflow.log_metric("latency_seconds", latency)
        mlflow.log_metric("original_length", len(message))
        mlflow.log_metric("translation_length", len(translated))

        mlflow.log_text(message, "original_text.txt")
        mlflow.log_text(translated, "translated_text.txt")

    return translated


if __name__ == "__main__":
    PROVIDERS = ["Google", "OpenRouter"]
    MODELS = {
        "OpenRouter": ["deepseek/deepseek-chat-v3.1:free"],
        "Google": ["gemini-2.5-flash-lite"],
    }
    LANGUAGES = [
        "English", "Mandarin Chinese", "Hindi", "Spanish", "French",
        "Modern Standard Arabic", "Bengali", "Portuguese", "Russian",
        "Urdu", "Indonesian", "German", "Japanese", "Swahili",
        "Turkish", "Tamil", "Vietnamese", "Italian", "Korean"
    ]

    def update_models(provider):
        return gr.Dropdown(choices=MODELS[provider], value=MODELS[provider][0])

    def chat_with_config(message, history, provider, model, target_language):
        return chat(message, history, provider, model, target_language)


    with gr.Blocks() as demo:
        gr.Markdown("# 🌍 AI Translator\nTraduce texto usando OpenRouter o Gemini.")

        with gr.Row():
            provider = gr.Dropdown(PROVIDERS, label="Provider", value=PROVIDERS[0])
            model = gr.Dropdown(MODELS[PROVIDERS[0]], label="Model", value=MODELS[PROVIDERS[0]][0])
            target = gr.Dropdown(
                choices=LANGUAGES,
                label="Idioma objetivo",
                value="Spanish",
                allow_custom_value=True
            )

        provider.change(update_models, provider, model)

        chatbot = gr.ChatInterface(
            fn=chat_with_config,
            additional_inputs=[provider, model, target],
            type="messages"
        )

    print("-------")
    demo.launch(server_name="0.0.0.0", server_port=7860)