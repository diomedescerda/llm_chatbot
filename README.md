# 🚀 Translation App + MLflow (Docker)

This project runs two containers:

1. **MLflow Tracking Server**
2. **Translation App** (Gradio + MLflow logging)

Both containers communicate through a shared Docker network called **`mlflow-net`**.

---

## 🧱 1. Create the Docker Network

```bash
docker network create mlflow-net
```

---

## 📦 2. Start MLflow Server

```bash
docker run -d \
  --name mlflow-server \
  --network mlflow-net \
  -p 5000:5000 \
  -v mlflow-data:/mlflow \
  ghcr.io/mlflow/mlflow:latest \
  mlflow server \
    --host 0.0.0.0 \
    --port 5000 \
    --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root /mlflow \
    --allowed-hosts="*"
```

### ✔ What this does

* Hosts MLflow at **[http://localhost:5000](http://localhost:5000)**
* Stores experiments in a SQLite file (`mlflow.db`)
* Saves artifacts in a persistent Docker volume (`mlflow-data`)
* Allows connections from any host *inside the Docker network* (`--allowed-hosts="*"`)

---

## 🌐 3. Start the Translation App

```bash
docker run -d \
  --name translator \
  --network mlflow-net \
  -p 7860:7860 \
  translation_app:latest
```

### ✔ What this does

* Runs your translation app on **[http://localhost:7860](http://localhost:7860)**
* Connects to MLflow via the shared network (`mlflow-net`)

Your `app.py` should contain:

```python
mlflow.set_tracking_uri("http://mlflow-server:5000")
```

---

## ✅ Access the Tools

| Service            | URL                                            |
| ------------------ | ---------------------------------------------- |
| MLflow UI          | [http://localhost:5000](http://localhost:5000) |
| Translation App UI | [http://localhost:7860](http://localhost:7860) |