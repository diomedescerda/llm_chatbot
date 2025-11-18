# 🚀 Translation App + MLflow (Docker Compose + Docker Swarm)

This project provides a fully containerized setup for:
1. **MLflow Tracking Server**
2. **Translation App** (Gradio + MLflow logging)

You can run it in two modes:
- **MLflow Tracking Server**
- **Translation App** (Gradio + MLflow logging)

---
⚠️ **Important:**
Before running the app by any method, ensure you provide your API key (for the model provider) in one of the following ways:

- As an environment variable:
```bash
export API_KEY="your_key_here"
```
---

## 🐳 1. Run with Docker Compose (LOCAL)
Docker Compose builds locally and is ideal for development.

```bash
docker compose up --build -d
```

This will:
- **Build the app-traductor image**
- **Start MLflow server**
- **Start the translation app**
- **Create the Docker network automatically**
---

## 🐳 2. Deploy with Docker Swarm (PRODUCTION)

1. **Initialize Swarm (only once)**
```bash
docker swarm init
```

2. **Deploy the stack**
```bash
docker stack deploy -c docker-stack.yml traductor-stack
```

3. **Check running services**
```bash
docker stack services traductor-stack
```
---

## ✅ Access the Apps

| Service            | URL                                            |
| ------------------ | ---------------------------------------------- |
| MLflow UI          | [http://localhost:5000](http://localhost:5000) |
| Translation App UI | [http://localhost:7860](http://localhost:7860) |
