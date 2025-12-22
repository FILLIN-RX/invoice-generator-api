FROM python:3.11-slim

# 1️⃣ Dépendances système pour WeasyPrint
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    fonts-dejavu \
    && rm -rf /var/lib/apt/lists/*

# 2️⃣ Dossier de travail
WORKDIR /app

# 3️⃣ Dépendances Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4️⃣ Code
COPY . .

# 5️⃣ Port Render
EXPOSE 8000

# 6️⃣ Lancer FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
