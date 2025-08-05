# Folosește o imagine oficială Python slim
FROM python:3.12-slim

# Setează directorul de lucru din container
WORKDIR /app

# Copiază requirements.txt și instalează dependențele
COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

# Copiază întregul cod sursă în container
COPY . .

# Expune portul pe care rulează FastAPI
EXPOSE 8000

# Pornește aplicația
CMD ["uvicorn", "app.main:app", "--host", "localhost", "--port", "8000"]