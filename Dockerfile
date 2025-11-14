# ---- Base image ----
FROM python:3.12-slim

# Prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Workdir ----
WORKDIR /app

# ---- Copy files ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Set the MLFLOW_TRACKING_URI environment variable
ENV MLFLOW_TRACKING_URI=http://mlflow-server:5000 

# ---- Expose Gradio ----
EXPOSE 7860

# ---- Start the app ----
CMD ["python", "app.py"]