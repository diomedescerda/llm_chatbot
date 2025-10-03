from openai import OpenAI

open_router = OpenAI(base_url="https://openrouter.ai/api/v1", api_key="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")
open_model_name = "deepseek/deepseek-chat-v3.1:free"

gemini = OpenAI(base_url="https://generativelanguage.googleapis.com/v1beta/openai/", api_key="AIzaSyCccnhjFvWqkYPh3uoRVnQQjH5kc52RNW4")
gemini_model_name = "models/learnlm-2.0-flash-experimental"


def chat(message, history):
    try:
        messages = [
            {
                "role": "system",
                "content": "Eres un traductor.",
            },
            {
                "role": "system",
                "content": "Eres un asistente que realiza resumenes de textos.",
            }
        ]

        for msg in history:
            if msg["role"] == "user":
                messages.append({"role": "user", "content": msg["content"]})
            elif msg["role"] == "assistant":
                messages.append({"role": "assistant", "content": msg["content"]})

        messages.append({"role": "user", "content": message})

        

        resp = ollama.chat.completions.create(
            model=model_name,
            messages=messages,
        )
        return resp.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return f"Error: {e}"


if __name__ == "__main__":
    import gradio as gr

    PROVIDERS = ["OpenRouter", "Google"]
    MODELS = {
        "OpenRouter": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        "Google": ["claude-2", "claude-instant", "claude-3-opus"],
    }
    TASKS = ["General Chat", "Code Generation", "Content Writing", "Analysis", "Translation"]

    def update_models(provider):
        return gr.Dropdown(choices=MODELS[provider], value=MODELS[provider][0])

    def chat_with_config(message, history, provider, model, task):
        # Your chat implementation here
        # Use provider, model, and task parameters
        response = f"[{provider}/{model}] {task}: {message}"
        return response

    if __name__ == "__main__":
        with gr.Blocks() as demo:
            gr.Markdown("## Chat Interface with Configuration")
            
            with gr.Row():
                provider = gr.Dropdown(PROVIDERS, label="Provider", value=PROVIDERS[0])
                model = gr.Dropdown(MODELS[PROVIDERS[0]], label="Model", value=MODELS[PROVIDERS[0]][0])
                task = gr.Dropdown(TASKS, label="Task", value=TASKS[0])
            
            provider.change(update_models, provider, model)
            
            chatbot = gr.ChatInterface(
                fn=lambda message, history: chat_with_config(
                    message, history, provider.value, model.value, task.value
                ),
                additional_inputs=[provider, model, task],
                type="messages"
            )
        
        demo.launch()